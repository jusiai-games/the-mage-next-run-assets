$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$asset=Join-Path $PSScriptRoot '../../exports/v1/wood-spell-cards'
$cards=@('CardFire','CardLightning','CardIce','CardWind') | ForEach-Object {
    [Drawing.Bitmap]::new((Join-Path $asset "$_.png"))
}
$burn=[Drawing.Bitmap]::new((Join-Path $asset 'sacrifice/embers-mask.png'))
$embers=[Drawing.Bitmap]::new((Join-Path $asset 'sacrifice/embers-overlay.png'))
$themes=@(
    @{name='불씨 전달'; color='#ffb65f'; second='#765043'},
    @{name='룬 재각인'; color='#d5b5fa'; second='#654f82'},
    @{name='숫자 뒤집기'; color='#a9eddb'; second='#3d777c'}
)
function Center($x,$y,$value,$size,$ink){
    $f=[Drawing.Font]::new('Malgun Gothic',$size,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
    $b=Brush $ink
    $format=[Drawing.StringFormat]::new()
    $format.Alignment='Center'
    $g.DrawString([string]$value,$f,$b,[single]$x,[single]$y,$format)
    $f.Dispose(); $b.Dispose(); $format.Dispose()
}
function Outline($x,$y,$w,$h,$color){
    $pen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($color),2)
    $g.DrawRectangle($pen,$x,$y,$w,$h)
    $pen.Dispose()
}
for($f=0;$f -lt 68;$f++){
    $b=[Drawing.Bitmap]::new(646,734)
    $g=[Drawing.Graphics]::FromImage($b)
    $g.Clear([Drawing.ColorTranslator]::FromHtml('#171c29'))
    $g.InterpolationMode='NearestNeighbor'
    $g.PixelOffsetMode='Half'
    $g.TextRenderingHint='AntiAliasGridFit'
    Label 19 10 '카드 희생 · 숫자 변경 시안' 24 '#ffe5bd' $true
    for($i=0;$i -lt 3;$i++){
        $theme=$themes[$i]
        $y=53+225*$i
        Rect 19 $y 608 213 '#242940'
        Rect 19 $y 608 1 $theme.color
        Label 32 ($y+10) $theme.name 20 '#ffe9ce' $true
        $status=if($f -lt 23){'화염구 희생'}elseif($f -lt 40){'숫자를 바꿀 카드를 고르세요'}elseif($f -lt 48){'연쇄 번개 숫자 변경 중'}else{'연쇄 번개 · 3 → 5'}
        Label 32 ($y+40) $status 14 $theme.color $true
        for($j=0;$j -lt 4;$j++){
            $x=115+$j*116
            $cardY=$y+73
            $name=@('화염구','연쇄 번개','빙창','돌풍')[$j]
            $n=@(4,3,2,1)[$j]
            if($j -eq 0){
                if($f -ge 23){continue}
                $sx=($f%8)*80; $sy=[int][math]::Floor($f/8)*94
                $masked=[Drawing.Bitmap]::new(44,64)
                $maskG=[Drawing.Graphics]::FromImage($masked)
                $maskG.DrawImageUnscaled($cards[0],0,0)
                $display=$g; $g=$maskG
                Center 22 37 $name 5 '#fff2df'
                Center 22 47 4 9 '#3e2c31'
                $g=$display
                $maskG.Dispose()
                for($py=0;$py -lt 64;$py++){
                    for($px=0;$px -lt 44;$px++){
                        if($burn.GetPixel($sx+18+$px,$sy+16+$py).A -eq 0){
                            $masked.SetPixel($px,$py,[Drawing.Color]::Transparent)
                        }
                    }
                }
                $g.DrawImage($masked,[Drawing.Rectangle]::new($x,$cardY,88,128))
                $masked.Dispose()
                $g.DrawImage($embers,[Drawing.Rectangle]::new(($x-36),($cardY-32),160,188),$sx,$sy,80,94,[Drawing.GraphicsUnit]::Pixel)
                continue
            }
            if($f -ge 23 -and $f -lt 40){
                $border=if($f%12 -lt 7){$theme.color}else{$theme.second}
                if($i -ne 2){
                    Outline ($x-2) ($cardY-2) 91 131 $border
                }
            }
            $g.DrawImage($cards[$j],[Drawing.Rectangle]::new($x,$cardY,88,128))
            Center ($x+44) ($cardY+74) $name 11 '#fff2df'
            if($f -ge 23 -and $f -lt 40){
                if($i -eq 0){
                    $lift=[int](3*[math]::Sin(($f-23)*.4+$j))
                    Poly @(($x+44),($cardY-19+$lift),($x+49),($cardY-12+$lift),($x+44),($cardY-7+$lift),($x+39),($cardY-12+$lift)) $theme.color
                }elseif($i -eq 1){
                    Center ($x+44) ($cardY-22) '◇' 17 $theme.color
                }else{
                    Outline ($x+21) ($cardY+91) 46 29 $theme.color
                }
            }
            if($j -eq 1 -and $f -ge 40){
                if($f -lt 51){Outline ($x-2) ($cardY-2) 91 131 $theme.color}
                $t=$f-40
                if($t -lt 12){
                    switch($i){
                        0 {
                            for($k=0;$k -lt 8;$k++){
                                $px=$x+44-[int]((12-$t)*(5+$k%2))+$k*3
                                $py=$cardY+107+[int]([math]::Sin(($k+$t)*.65)*12)
                                Rect $px $py (2+$k%3) 2 $theme.color
                            }
                        }
                        1 {
                            $r=31-2*$t
                            $pen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($theme.second),2)
                            $g.DrawEllipse($pen,($x+44-$r),($cardY+107-[int]($r/2)),(2*$r),$r)
                            $pen.Dispose()
                        }
                        2 {
                            $h=[math]::Max(2,18-4*[math]::Abs(6-$t))
                            Rect ($x+28) ($cardY+108-[int]($h/2)) 32 $h $theme.color
                        }
                    }
                }
                if($t -ge 8){$n=5}
                if($t -ge 8){
                    Center ($x+44) ($cardY+91) '3 → 5' 21 '#3e2c31'
                }elseif($i -ne 2 -or $t -lt 3){
                    Center ($x+44) ($cardY+91) $n 21 '#3e2c31'
                }
            }else{
                Center ($x+44) ($cardY+91) $n 21 '#3e2c31'
            }
        }
    }
    $g.Dispose()
    if($f -eq 28){$b.Save((Join-Path $PSScriptRoot 'choose.png'),[Drawing.Imaging.ImageFormat]::Png)}
    if($f -eq 49){$b.Save((Join-Path $PSScriptRoot 'changed.png'),[Drawing.Imaging.ImageFormat]::Png)}
    $b.Save((Join-Path $PSScriptRoot ('review/frame-{0:D2}.png' -f $f)),[Drawing.Imaging.ImageFormat]::Png)
    $b.Dispose()
}
foreach($card in $cards){$card.Dispose()}
$burn.Dispose(); $embers.Dispose()
& ffmpeg -hide_banner -loglevel error -y -framerate 20 -i (Join-Path $PSScriptRoot 'review/frame-%02d.png') -vf 'split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none' -loop 0 (Join-Path $PSScriptRoot 'comparison.gif')
if($LASTEXITCODE -ne 0){throw 'GIF encoding failed.'}

