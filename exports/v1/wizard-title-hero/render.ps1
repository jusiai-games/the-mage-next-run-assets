param([Parameter(Mandatory)][string]$Source)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$out=$PSScriptRoot
$legacy=Join-Path $out '../wizard'
$image=[Drawing.Bitmap]::new($Source)
$colors='#16131b','#35242d','#512c2b','#703832','#92463a','#b45d43','#e68e52','#ffbf77',
        '#613b28','#935930','#c88c4c','#f3be67','#34283f','#4c3c60','#705986','#9275a5',
        '#9f654e','#d29069','#f1b48a','#ffd5a6','#f3e8d8','#38313b','#76656b',
        '#18474b','#287a7c','#4fcac6','#a2f1e4','#edfff5'
$palette=foreach($hex in $colors){[Drawing.ColorTranslator]::FromHtml($hex)}
function New-Cell { [Drawing.Bitmap]::new(32,32) }
function Read-Pose($left,$top,$width,$height,$targetHeight,$offset) {
    $cell=New-Cell
    $targetWidth=[int][Math]::Round($width*$targetHeight/$height)
    for($y=0;$y -lt $targetHeight;$y++){
        for($x=0;$x -lt $targetWidth;$x++){
            $sx=[int][Math]::Floor($left+($x+0.5)*$width/$targetWidth)
            $sy=[int][Math]::Floor($top+($y+0.5)*$height/$targetHeight)
            $sample=$image.GetPixel($sx,$sy)
            if($sample.A -lt 128){continue}
            $distance=[double]::PositiveInfinity
            foreach($color in $palette){
                $dr=$sample.R-$color.R; $dg=$sample.G-$color.G; $db=$sample.B-$color.B
                $score=2*$dr*$dr+3*$dg*$dg+2*$db*$db
                if($score -lt $distance){$distance=$score;$chosen=$color}
            }
            $cell.SetPixel(($x+$offset),($y+28-$targetHeight),$chosen)
        }
    }
    $cell
}
function Put($cell,$x,$y,$hex) {
    $cell.SetPixel($x,$y,[Drawing.ColorTranslator]::FromHtml($hex))
}
function Staff($cell,$x0,$y0,$x1,$y1) {
    $steps=[Math]::Max([Math]::Abs($x1-$x0),[Math]::Abs($y1-$y0))
    for($i=0;$i -le $steps;$i++){
        $x=[int][Math]::Round($x0+($x1-$x0)*$i/$steps)
        $y=[int][Math]::Round($y0+($y1-$y0)*$i/$steps)
        Put $cell $x $y '#c88c4c'
        Put $cell $x ($y+1) '#613b28'
    }
    Put $cell $x1 $y1 '#a2f1e4'
    Put $cell ($x1-1) ($y1-1) '#4fcac6'
    Put $cell ($x1-1) $y1 '#edfff5'
}
function Move-ShaftRow($cell,[int]$y,[int]$left,[int]$right,[int]$dx) {
    $pixels=for($x=$left;$x -le $right;$x++){$cell.GetPixel($x,$y)}
    for($x=$left;$x -le $right;$x++){$cell.SetPixel($x,$y,[Drawing.Color]::Transparent)}
    for($i=0;$i -lt $pixels.Count;$i++){
        if($pixels[$i].A -eq 255){$cell.SetPixel(($left+$i+$dx),$y,$pixels[$i])}
    }
}
function Copy-StaffHead($cell,$base,[int]$dx,[int]$dy) {
    # Copy the original faceted jewel and socket at their native pixel size.
    for($y=8;$y -le 15;$y++){
        $left=if($y -eq 11){22}elseif($y -ge 13){21}else{22}
        for($x=$left;$x -le 24;$x++){
            $pixel=$base.GetPixel($x,$y)
            if($pixel.A -eq 255){$cell.SetPixel(($x+$dx),($y+$dy),$pixel)}
        }
    }
}
function Breathe($base,[bool]$lighten) {
    $cell=[Drawing.Bitmap]$base.Clone()
    # An interior fold changes shade while the shoulder, head and feet stay joined.
    for($y=14;$y -le 17;$y++){
        for($x=10;$x -le 13;$x++){
            $name=$base.GetPixel($x,$y).Name
            if($lighten -and $name -eq 'ff4c3c60'){Put $cell $x $y '#705986'}
            if(!$lighten -and $name -eq 'ff705986'){Put $cell $x $y '#4c3c60'}
        }
    }
    $cell
}
function Match-Head($cell,$base,[int]$dx,[int]$dy,[int]$cutoff) {
    # All upright poses use the same hand-approved face and hair pixels.
    for($y=0;$y -le 12+$dy;$y++){
        for($x=0;$x -le $cutoff;$x++){ $cell.SetPixel($x,$y,[Drawing.Color]::Transparent) }
    }
    for($y=2;$y -le 12;$y++){
        for($x=9;$x -le 21;$x++){
            if($x -eq 21 -and $y -ge 10){continue}
            $p=$base.GetPixel($x,$y)
            if($p.A -eq 255){$cell.SetPixel(($x+$dx),($y+$dy),$p)}
        }
    }
}
function Remove-Flecks($cell) {
    # Keep the connected silhouette. Diagonal neighbors belong to the same outline.
    $seen=[bool[]]::new(1024)
    $largest=@()
    for($i=0;$i -lt 896;$i++){
        if($seen[$i] -or !$cell.GetPixel(($i%32),[int][Math]::Floor($i/32)).A){continue}
        $queue=[Collections.Generic.List[int]]::new()
        $queue.Add($i)
        $seen[$i]=$true
        for($k=0;$k -lt $queue.Count;$k++){
            $x=$queue[$k]%32
            $y=[int][Math]::Floor($queue[$k]/32)
            foreach($ny in ([Math]::Max(0,$y-1))..([Math]::Min(27,$y+1))){
                foreach($nx in ([Math]::Max(0,$x-1))..([Math]::Min(31,$x+1))){
                    $j=$ny*32+$nx
                    if(!$seen[$j] -and $cell.GetPixel($nx,$ny).A){
                        $seen[$j]=$true
                        $queue.Add($j)
                    }
                }
            }
        }
        if($queue.Count -gt $largest.Count){$largest=$queue}
    }
    $keep=[Collections.Generic.HashSet[int]]::new()
    foreach($pixel in $largest){[void]$keep.Add($pixel)}
    for($i=0;$i -lt 896;$i++){
        if($seen[$i] -and !$keep.Contains($i)){
            $cell.SetPixel(($i%32),[int][Math]::Floor($i/32),[Drawing.Color]::Transparent)
        }
    }
}
function Hit-Pose($base) {
    $cell=New-Cell
    for($y=0;$y -lt 28;$y++){
        for($x=1;$x -lt 32;$x++){
            $pixel=$base.GetPixel($x,$y)
            if($pixel.A -eq 255){$cell.SetPixel(($x-1),$y,$pixel)}
        }
    }
    $cell
}
function Sharpen-Outline($cell) {
    $source=[Drawing.Bitmap]$cell.Clone()
    for($y=1;$y -lt 28;$y++){
        for($x=1;$x -lt 31;$x++){
            $pixel=$source.GetPixel($x,$y)
            if($pixel.A -eq 0){continue}
            $left=$source.GetPixel(($x-1),$y)
            $right=$source.GetPixel(($x+1),$y)
            $up=$source.GetPixel($x,($y-1))
            $down=$source.GetPixel($x,($y+1))
            $openEdges=0
            foreach($neighbor in @($left,$right,$up,$down)){if(!$neighbor.A){$openEdges++}}
            if($openEdges -eq 0){continue}
            $darkEdge=$pixel.Name -in @('ff35242d','ff34283f','ff38313b','ff512c2b')
            $weakCorner=$openEdges -ge 2 -and $pixel.Name -in @('ff4c3c60','ff613b28','ff703832')
            if($darkEdge -or $weakCorner){Put $cell $x $y '#16131b'}
        }
    }
    $source.Dispose()
}
function Fall-Pose($base,[double]$angle,[int]$centerX,[int]$centerY) {
    $cell=New-Cell
    $r=$angle*[Math]::PI/180
    $cos=[Math]::Cos($r);$sin=[Math]::Sin($r)
    for($y=0;$y -lt 28;$y++){
        for($x=0;$x -lt 32;$x++){
            $dx=$x-$centerX;$dy=$y-$centerY
            $sx=[int][Math]::Round(15+$cos*$dx+$sin*$dy)
            $sy=[int][Math]::Round(14-$sin*$dx+$cos*$dy)
            if($sx -lt 0 -or $sx -gt 31 -or $sy -lt 0 -or $sy -gt 31){continue}
            $p=$base.GetPixel($sx,$sy)
            if($p.A -eq 255){$cell.SetPixel($x,$y,$p)}
        }
    }
    $cell
}
$base=Read-Pose 24 31 467 636 26 6
$walk1=Read-Pose 550 27 208 254 26 5
$walk2=Read-Pose 762 27 218 260 26 5
$walk3=Read-Pose 970 27 194 260 26 5
$walk4=Read-Pose 1174 27 181 260 26 5
$brace=Read-Pose 518 369 273 259 26 3
$release=Read-Pose 1760 380 221 242 26 4
$recover=Read-Pose 1457 366 236 263 26 3
Staff $release 16 16 28 14
Staff $recover 17 20 27 8
Match-Head $walk1 $base 0 1 20
Match-Head $walk2 $base 1 1 22
Match-Head $walk3 $base 1 1 22
Match-Head $walk4 $base 1 1 22
Match-Head $brace $base 1 1 22
Match-Head $release $base 2 1 23
Match-Head $recover $base 0 1 21
# Preserve the ground contact during the forward lean at the release key.
for($x=0;$x -lt 32;$x++){
    $sole=$release.GetPixel($x,26)
    if($sole.A -eq 255){Put $release $x 27 '#16131b'}
}
# The original crystal and socket stay fixed; only the shaft below is aligned.
Move-ShaftRow $base 13 20 22 1
Move-ShaftRow $base 14 20 21 1
Move-ShaftRow $base 15 20 21 1
Put $base 22 16 '#935930'
Move-ShaftRow $walk1 15 20 23 1
Move-ShaftRow $walk1 16 20 23 1
Move-ShaftRow $walk2 16 20 22 1
# The two source walk poses without a staff borrow the same detailed head.
Copy-StaffHead $walk3 $base 1 1
Copy-StaffHead $walk4 $base 1 2
foreach($y in 17..20){Put $walk3 23 $y '#935930'}
foreach($y in 18..22){Put $walk4 23 $y '#935930'}
Put $walk3 22 17 '#d29069'
Put $walk4 22 19 '#d29069'
# Preserve the previous waist fix without merging the material color ramps.
foreach($x in 10..13){Put $base $x 17 '#4c3c60'}
Put $base 14 17 '#35242d'
foreach($x in 15..18){Put $base $x 17 '#613b28'}
function Close-Grip($pose,[int]$x,[int]$y) {
    # Join the sleeve to the grip, with the fingers crossing the shaft.
    Put $pose ($x-2) $y '#4c3c60'
    Put $pose ($x-1) ($y-1) '#16131b'
    Put $pose ($x-1) $y '#f1b48a'
    Put $pose $x $y '#d29069'
    Put $pose ($x-1) ($y+1) '#9f654e'
}
function Walk-PassingPose($from,$to,[bool]$leadRight) {
    $cell=[Drawing.Bitmap]$from.Clone()
    # Keep the shoulder, arm and prop together; pose the passing feet separately.
    for($y=23;$y -le 27;$y++){
        for($x=7;$x -le 23;$x++){
            $split=16
            $useNext=($x -ge $split) -eq $leadRight
            if($useNext){
                $pixel=$to.GetPixel($x,$y)
                $cell.SetPixel($x,$y,$pixel)
            }
        }
    }
    $cell
}
function Cast-Inbetween($pose,[int]$moveDirection) {
    $cell=[Drawing.Bitmap]$pose.Clone()
    # Shift the hand and crystal together, shearing the upper part by at most one pixel.
    for($y=7;$y -le 19;$y++){
        $anchor=if($y -le 13){22}else{20}
        for($x=$anchor;$x -le 30;$x++){ $cell.SetPixel($x,$y,[Drawing.Color]::Transparent) }
    }
    for($y=7;$y -le 19;$y++){
        $anchor=if($y -le 13){22}else{20}
        $dy=if($y -lt 14){$moveDirection}else{0}
        $dx=if($y -ge 14){-$moveDirection}else{0}
        for($x=$anchor;$x -le 30;$x++){
            $pixel=$pose.GetPixel($x,$y)
            if($pixel.A -eq 255){$cell.SetPixel(($x+$dx),($y+$dy),$pixel)}
        }
    }
    $cell
}
# Align the grip on each source pose before deriving the new keys.
Close-Grip $walk1 21 17
Close-Grip $walk2 22 16
Close-Grip $walk3 23 17
Close-Grip $walk4 23 19
Close-Grip $brace 22 15
Close-Grip $release 25 15
Close-Grip $recover 22 14
$walkMid1=Walk-PassingPose $walk1 $walk3 $true
$walkMid2=Walk-PassingPose $walk3 $walk2 $true
$walkMid3=Walk-PassingPose $walk2 $walk4 $false
$walkMid4=Walk-PassingPose $walk4 $walk1 $false
$castFollow=Cast-Inbetween $release -1
# Keep the release crystal and timber connected during the follow-through.
for($y=13;$y -le 16;$y++){
    for($x=24;$x -le 28;$x++){
        $pixel=$release.GetPixel($x,$y)
        if($pixel.A -eq 255){$castFollow.SetPixel($x,$y,$pixel)}
    }
}
Close-Grip $castFollow 25 15
$castLower=Cast-Inbetween $recover 1
Close-Grip $castLower 21 15
$castSettle=Cast-Inbetween $base -1
Close-Grip $castSettle 22 17
$clips=[ordered]@{
    idle=@($base,(Breathe $base $true),$base,(Breathe $base $false),$base)
    walk=@($walk1,$walk3,$walk2,$walk4,$walkMid1,$walkMid2,$walkMid3,$walkMid4)
    cast=@($base,$brace,$release,$recover,$base,$castFollow,$castLower,$castSettle)
    fall=@($base,(Hit-Pose $base),(Fall-Pose $base -19 14 16),(Fall-Pose $base -38 13 17),(Fall-Pose $base -63 13 17),(Fall-Pose $base -90 14 21))
}
$preview=[Drawing.Bitmap]::new(840,384)
$pg=[Drawing.Graphics]::FromImage($preview)
$pg.Clear([Drawing.ColorTranslator]::FromHtml('#354255'))
$pg.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$pg.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
$order=@{walk=@(0,4,1,5,2,6,3,7);cast=@(0,1,2,5,3,6,7,4)}
$row=0
$labels=@{idle='대기';walk='걷기';cast='시전';fall='쓰러짐'}
$font=[Drawing.Font]::new('Malgun Gothic',15,[Drawing.GraphicsUnit]::Pixel)
foreach($clip in $clips.Keys){
    $pg.DrawString($labels[$clip],$font,[Drawing.Brushes]::White,12,($row*96+38))
    $frames=$clips[$clip]
    $folder=Join-Path $out $clip
    New-Item -ItemType Directory -Force $folder | Out-Null
    $name="title_hero_$clip"
    $sheet=[Drawing.Bitmap]::new(($frames.Count*32),32)
    $graphics=[Drawing.Graphics]::FromImage($sheet)
    $sprites=for($i=0;$i -lt $frames.Count;$i++){
        $frame=$frames[$i]
        if($clip -eq "walk" -or ($clip -eq "fall" -and $i -gt 0) -or ($clip -eq "cast" -and $i -notin 0,4)){Remove-Flecks $frame}
        Sharpen-Outline $frame
        $graphics.DrawImageUnscaled($frame,($i*32),0)
        $column=if($order.ContainsKey($clip)){[array]::IndexOf($order[$clip],$i)}else{$i}
        $pg.DrawImage($frame,[Drawing.Rectangle]::new((72+$column*96),($row*96),96,96))
        @{name=('{0}_right_{1:D2}' -f $name,$i);x=$i*32;y=0}
    }
    $graphics.Dispose()
    $path=Join-Path $folder "$name.png"
    $sheet.Save($path,[Drawing.Imaging.ImageFormat]::Png)
    $sheet.Dispose()
    $manifest=[ordered]@{version=1;kind='character';width=$frames.Count*32;height=32;cell=32;ppu=32;pivotX=0.5;pivotY=0.125;sha256=(Get-FileHash $path).Hash.ToLowerInvariant();sprites=@($sprites)}
    $manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 (Join-Path $folder "$name.sprite.json")
    $timing=Get-Content -Raw -Encoding utf8 (Join-Path $legacy "$clip/timing.json") | ConvertFrom-Json
    $timing.PSObject.Properties.Remove('source_frame_order_zero_based')
    $timing.PSObject.Properties.Remove('frame_x_offset_px')
    if($clip -eq 'walk'){
        $timing.samples_per_second=20
        $timing.frame_durations_ms=@(50,50,50,50,50,50,50,50)
    }
    if($clip -eq 'cast'){
        $timing.key_samples=@(0,1,3,4,5,6,7,8)
        $timing | Add-Member -Force NoteProperty unity_release_frame_order_zero_based @(2,5,3,6,7,4)
    }
    if($order.ContainsKey($clip)){
        $timing | Add-Member -Force NoteProperty playback_frame_order_zero_based $order[$clip]
    }
    $timing | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 (Join-Path $folder 'timing.json')
    $row++
}
$preview.Save((Join-Path $out 'preview.png'),[Drawing.Imaging.ImageFormat]::Png)
$font.Dispose()
$pg.Dispose()
$preview.Dispose()
$image.Dispose()




















