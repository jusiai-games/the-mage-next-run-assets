$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
New-Item -ItemType Directory -Force (Join-Path $PSScriptRoot 'review/flame') | Out-Null
$asset=Join-Path $PSScriptRoot '../../exports/v1/wood-spell-cards'
$cards=@('CardLightning','CardIce','CardWind') | ForEach-Object {
    [Drawing.Bitmap]::new((Join-Path $asset "$_.png"))
}
function TextCenter($x,$y,$value,$size,$ink,$outline=$false){
    $f=[Drawing.Font]::new('Malgun Gothic',$size,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
    $b=Brush $ink
    $fmt=[Drawing.StringFormat]::new()
    $fmt.Alignment='Center'
    if($outline){
        $edge=Brush '#fff0b7'
        foreach($offset in @(@(-1,0),@(1,0),@(0,-1),@(0,1))){
            $g.DrawString($value,$f,$edge,[single]($x+$offset[0]),[single]($y+$offset[1]),$fmt)
        }
        $edge.Dispose()
    }
    $g.DrawString($value,$f,$b,[single]$x,[single]$y,$fmt)
    $f.Dispose(); $b.Dispose(); $fmt.Dispose()
}
for($f=0;$f -lt 58;$f++){
    $b=[Drawing.Bitmap]::new(650,347)
    $g=[Drawing.Graphics]::FromImage($b)
    $g.Clear([Drawing.ColorTranslator]::FromHtml('#171c29'))
    $g.InterpolationMode='NearestNeighbor'
    $g.PixelOffsetMode='Half'
    $g.TextRenderingHint='AntiAliasGridFit'
    Label 24 16 '불씨 전달 · 숫자 변경' 25 '#ffe5bd' $true
    $status=if($f -lt 12){'숫자를 바꿀 카드를 고르세요'}elseif($f -lt 29){'연쇄 번개 숫자 변경 중'}else{'연쇄 번개 · 숫자 변경 완료'}
    Label 25 53 $status 15 '#ffc174' $true
    Rect 24 90 602 231 '#252840'
    for($j=0;$j -lt 3;$j++){
        $x=108+$j*162
        $y=109
        if(($f -lt 12 -or ($j -eq 0 -and $f -lt 34))){
            $glow=if($f%8 -lt 5){'#efaa5b'}else{'#9b684d'}
            Rect ($x-2) ($y-2) 136 196 $glow
        }
        $g.DrawImage($cards[$j],[Drawing.Rectangle]::new($x,$y,132,192))
        TextCenter ($x+66) ($y+109) (@('연쇄 번개','빙창','돌풍')[$j]) 17 '#fff2df'
        if($j -gt 0){
            TextCenter ($x+66) ($y+139) (@('3','2','1')[$j]) 27 '#3e2c31'
            continue
        }
        if($f -lt 25){
            $clip=$g.Save()
            if($f -ge 16){
                $scan=143+($f-16)*7
                $g.SetClip([Drawing.Rectangle]::new($scan,($y+135),([math]::Max(0,$x+110-$scan)),48))
            }
            TextCenter ($x+66) ($y+139) '3' 27 '#3e2c31'
            $g.Restore($clip)
        }
        if($f -ge 27){
            $size=if($f -lt 32){39-($f-27)}else{34}
            TextCenter ($x+66) ($y+134) '5' $size '#a12e24' $true
        }
    }
    if($f -ge 16 -and $f -lt 25){
        $scan=143+($f-16)*7
        Rect ($scan-2) 250 5 35 '#d87249'
        Rect $scan 249 1 37 '#fff2b4'
        Rect ($scan-3) 249 7 2 '#ffc170'
        Rect ($scan-3) 284 7 2 '#ffc170'
    }
    if($f -ge 19 -and $f -lt 33){
        # Emit sparks from the scanned strokes of the sample glyph.
        $strokes=@(@(167,255),@(171,254),@(176,254),@(180,258),@(178,262),@(173,265),@(177,268),@(180,271),@(177,275),@(172,276),@(168,274))
        for($k=0;$k -lt $strokes.Count;$k++){
            $point=$strokes[$k]
            $birth=16+[int][math]::Ceiling(($point[0]-143)/7.0)
            $age=$f-$birth
            if($age -lt 0 -or $age -gt 8){continue}
            $px=$point[0]-[int]($age*(1+($k%3)*.35))
            $py=$point[1]-[int]($age*(.5+($k%4)*.3))
            $ink=if($age -lt 3){'#fff2ac'}elseif($age -lt 6){'#ffae5d'}else{'#c25a41'}
            Rect $px $py $(if($age -lt 4){2}else{1}) 2 $ink
        }
    }
    $g.Dispose()
    $b.Save((Join-Path $PSScriptRoot ('review/flame/frame-{0:D2}.png' -f $f)),[Drawing.Imaging.ImageFormat]::Png)
    if($f -eq 46){$b.Save((Join-Path $PSScriptRoot 'flame-result.png'),[Drawing.Imaging.ImageFormat]::Png)}
    $b.Dispose()
}
foreach($card in $cards){$card.Dispose()}
& ffmpeg -hide_banner -loglevel error -y -framerate 20 -i (Join-Path $PSScriptRoot 'review/flame/frame-%02d.png') -vf 'split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none' -loop 0 (Join-Path $PSScriptRoot 'flame-transfer.gif')
if($LASTEXITCODE -ne 0){throw 'GIF encoding failed'}



