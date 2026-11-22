$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Join-Path $PSScriptRoot '../..'
$inputSheet=[Drawing.Bitmap]::new((Join-Path $root 'exports/v1/wizard-title-hero/walk/title_hero_walk.png'))
$sheet=[Drawing.Bitmap]::new(320,32)
$graphics=[Drawing.Graphics]::FromImage($sheet)
# Playback order: two half steps, each with contact, passing and extension.
# Each entry gives the supporting and swinging ankle coordinates and sole rows.
$steps=@(
    @(18,27,11,27), @(17,27,12,26), @(16,27,13,25), @(15,27,14,25),
    @(14,27,15,25), @(13,27,16,25), @(12,27,17,26), @(11,27,18,27),
    @(11,27,18,27), @(12,26,17,27), @(13,25,16,27), @(14,25,15,27),
    @(15,25,14,27), @(16,25,13,27), @(17,26,12,27), @(18,27,11,27)
)
$sourceOrder=@(0,4,1,5,2,6,3,7)
# Keep two readable crossing keys in each half-step.
$reviewOrder=@(0,2,3,4,6,8,10,11,12,14)
function Copy-StepLeg($frame,[int]$ankle,[int]$sole,[bool]$near,[int]$pelvis){
    # Sample both leg silhouettes, including outlines and boots, from the
    # original wide-stance frame. Move each row as a solid strip.
    $nativeSole=if($near){26}else{27}
    $nativeAnkle=if($near){18}else{11}
    $nearLeft=@(15,15,16,17,17)
    $nearRight=@(19,19,20,21,21)
    $farLeft=@(11,10,10,9,9,9)
    $farRight=@(14,14,14,13,12,12)
    # The knee leads the lifted boot; the cloth fold follows the thigh angle.
    $hip=if($near){16}else{14}
    $hip+=$pelvis
    $sole=[Math]::Max(26,$sole)
    $ankle=[Math]::Clamp($ankle,12,17)
    $edge=$inputSheet.GetPixel(15,22)
    $shade=$inputSheet.GetPixel(16,23)
    $cloth=if($near){$inputSheet.GetPixel(16,22)}else{$inputSheet.GetPixel(14,23)}
    for($y=22;$y -le $sole;$y++){
        if($y -lt $sole-1){
            $kneeRow=$sole-2
            $weight=[Math]::Min(1,($y-21)/[Math]::Max(1,$kneeRow-21))
            $center=[int][Math]::Round($hip+($ankle-$hip)*$weight*0.85)
            foreach($dx in -2..2){
                $tone=if($dx -eq -2 -or $dx -eq 2){$edge}elseif($dx -lt 0){$shade}else{$cloth}
                $frame.SetPixel(($center+$dx),$y,$tone)
            }
            # Taper into the ankle at the lower edge of the knee.
            if($y -eq $kneeRow){
                $toward=[Math]::Sign($ankle-$center)
                if($toward){$frame.SetPixel(($center+2*$toward),$y,$shade)}
            }
            continue
        }
        $row=$nativeSole-($sole-$y)-22
        $left=if($near){$nearLeft[$row]}else{$farLeft[$row]}
        $right=if($near){$nearRight[$row]}else{$farRight[$row]}
        for($sx=$left;$sx -le $right;$sx++){
            $pixel=$inputSheet.GetPixel($sx,($row+22))
            if($pixel.A){$frame.SetPixel(($sx+$ankle-$nativeAnkle),$y,$pixel)}
        }
    }
}
# An extra pose splits the second upper-body key of each half stride.
$ticks=@(0,5,8,10,15,20,25,28,30,35)
$upperKeys=@(0,4,4,1,5,2,6,6,3,7)
# Rightmost cloak pixel per source frame on rows 22, 23 and 24.
$cloakEnds=@(@(11,10,10),@(11,0,0),@(9,7,0),@(10,9,0),
             @(11,10,10),@(11,0,0),@(9,9,0),@(10,10,10))
function New-WalkPose([int]$index) {
    $frame=[Drawing.Bitmap]::new(32,32)
    $step=$steps[$reviewOrder[$index]]
    $pelvis=@(0,1,1,1,0,0,-1,-1,-1,0)[$index]
    Copy-StepLeg $frame $step[2] $step[3] $false $pelvis
    Copy-StepLeg $frame $step[0] $step[1] $true $pelvis
    $key=$upperKeys[$index]
    for($y=0;$y -le 24;$y++){
        for($x=0;$x -lt 32;$x++){
            if($y -ge 22 -and $x -gt $cloakEnds[$key][$y-22] -and $x -lt 22){continue}
            $c=$inputSheet.GetPixel(($key*32+$x),$y)
            if($c.A){$offset=if($y -eq 21 -and $x -in 12..18){$pelvis}else{0}
                $frame.SetPixel(($x+$offset),$y,$c)
                if($offset){$frame.SetPixel($x,$y,$c)}}
        }
    }
    # Keep the visible knuckles contiguous as the free hand passes the sleeve.
    if($key -in 1,5){
        $frame.SetPixel(12,18,$inputSheet.GetPixel(14,20))
        $frame.SetPixel(11,19,$inputSheet.GetPixel(13,21))
        $frame.SetPixel(12,19,$inputSheet.GetPixel(14,21))
    }
    if($key -in 2,6){
        $frame.SetPixel(13,20,$inputSheet.GetPixel(16,23))
        $frame.SetPixel(16,20,$inputSheet.GetPixel(15,22))
        $frame.SetPixel(16,21,$inputSheet.GetPixel(15,22))
    }
    $frame
}
for($i=0;$i -lt $reviewOrder.Count;$i++){
    $frame=New-WalkPose $i
    $graphics.DrawImageUnscaled($frame,(32*$i),0)
    $frame.Dispose()
}
$graphics.Dispose()
$sheet.Save((Join-Path $PSScriptRoot 'walk-review.png'),[Drawing.Imaging.ImageFormat]::Png)
$tmp=(New-Item -ItemType Directory -Force (Join-Path $root '.local/walk-review-frames')).FullName
for($tick=0;$tick -lt 40;$tick++){
    $i=0; while($i+1 -lt $ticks.Count -and $ticks[$i+1] -le $tick){$i++}
    $canvas=[Drawing.Bitmap]::new(278,148)
    $g=[Drawing.Graphics]::FromImage($canvas)
    $g.Clear([Drawing.ColorTranslator]::FromHtml('#354255'))
    $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
    $g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
    $font=[Drawing.Font]::new('Malgun Gothic',13,[Drawing.GraphicsUnit]::Pixel)
    $g.DrawString('복원한 버전',$font,[Drawing.Brushes]::White,13,6)
    $g.DrawString('전신 걷기 시안',$font,[Drawing.Brushes]::White,151,6)
    $g.DrawImage($inputSheet,[Drawing.Rectangle]::new(5,20,128,128),(32*$sourceOrder[[int][Math]::Floor($tick/5)]),0,32,32,[Drawing.GraphicsUnit]::Pixel)
    $g.DrawImage($sheet,[Drawing.Rectangle]::new(143,20,128,128),(32*$i),0,32,32,[Drawing.GraphicsUnit]::Pixel)
    $font.Dispose()
    $g.Dispose()
    $canvas.Save((Join-Path $tmp ('{0:D2}.png' -f $tick)),[Drawing.Imaging.ImageFormat]::Png)
    $canvas.Dispose()
}
$inputSheet.Dispose()
$sheet.Dispose()
$select=($ticks | ForEach-Object {"eq(n\,$_)"}) -join "+"
& ffmpeg -hide_banner -loglevel error -y -framerate 100 -i (Join-Path $tmp '%02d.png') -vf "select=$select,split[a][b];[a]palettegen[p];[b][p]paletteuse" -fps_mode vfr -frames:v 10 -final_delay 5 -loop 0 (Join-Path $PSScriptRoot 'comparison.gif')
if($LASTEXITCODE -ne 0){throw 'Could not encode comparison'}









