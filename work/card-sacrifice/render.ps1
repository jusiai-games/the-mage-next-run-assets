param([switch]$ExportEmbers)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly

$asset=Join-Path $PSScriptRoot '../../exports/v1/wood-spell-cards'
$preview=Join-Path $PSScriptRoot 'review'
New-Item -ItemType Directory -Force $preview | Out-Null
$cards=@{}
foreach($name in @('CardFire','CardIce','CardLightning')){
    $cards[$name]=[Drawing.Bitmap]::new((Join-Path $asset "$name.png"))
}
$concepts=@(
    @{id='embers'; title='불씨로 흩어짐'; note='아래에서 타오르며 재가 위로 날립니다.'; colors=@('#7d4144','#e16b49','#ffb768','#fff1bd')},
    @{id='rune'; title='룬으로 흡수'; note='카드가 가운데 인장으로 접혀 들어갑니다.'; colors=@('#574974','#a282c2','#dfbcf3','#fff0ff')},
    @{id='shards'; title='명판 파쇄'; note='나무 조각이 갈라져 아래로 떨어집니다.'; colors=@('#5a3b44','#ad785a','#dcb385','#f4d9aa')},
    @{id='dissolve'; title='마력으로 증발'; note='위에서부터 픽셀로 풀려 공중에 흩어집니다.'; colors=@('#375777','#5d9eaf','#93dfd4','#e9fff3')}
)
function Pixel($bitmap,$x,$y,$color){
    if($x -ge 0 -and $x -lt $bitmap.Width -and $y -ge 0 -and $y -lt $bitmap.Height){
        $bitmap.SetPixel($x,$y,$color)
    }
}
function EffectsFrame($theme,$frame,$layer="preview"){
    $b=[Drawing.Bitmap]::new(80,94)
    $palette=@($theme.colors | ForEach-Object {[Drawing.ColorTranslator]::FromHtml($_)})
    $card=$cards.CardFire
    if($frame -lt 4){
        $g=[Drawing.Graphics]::FromImage($b)
        if($layer -ne 'overlay'){
            $g.DrawImageUnscaled($card,18,16)
        }
        if($frame -ge 2 -and $layer -ne "mask"){
            $pen=[Drawing.Pen]::new($palette[2])
            $g.DrawRectangle($pen,17,15,45,65)
            $pen.Dispose()
        }
        $g.Dispose()
        return $b
    }
    $t=($frame-4)/15.0
    $rng=[Random]::new(1902)
    $g=[Drawing.Graphics]::FromImage($b)
    $g.InterpolationMode='NearestNeighbor'
    $g.PixelOffsetMode='Half'
    if($theme.id -eq 'rune'){
        if($t -lt .67){
            $w=[math]::Max(1,[int](44*(1-$t/.7)))
            $h=[math]::Max(1,[int](64*(1-$t/.72)))
            $g.DrawImage($card,[Drawing.Rectangle]::new((40-[int]($w/2)),(48-[int]($h/2)),$w,$h))
        }
        if($t -lt .92){
            $r=[int](8+19*[math]::Sin([math]::PI*$t))
            $pen=[Drawing.Pen]::new($palette[$(if($t -gt .73){0}else{2})])
            $g.DrawEllipse($pen,(40-$r),(48-$r),(2*$r),(2*$r))
            $pen.Dispose()
            foreach($a in 0,90,180,270){
                $a=($a+110*$t)*[math]::PI/180
                $x=40+[int]($r*[math]::Cos($a))
                $y=48+[int]($r*[math]::Sin($a))
                Poly @($x,($y-3),($x+3),$y,$x,($y+3),($x-3),$y) $theme.colors[3]
            }
        }
    }
    $g.Dispose()
    if($theme.id -ne 'rune'){
        for($y=0;$y -lt 64;$y++){
            for($x=0;$x -lt 44;$x++){
                $color=$card.GetPixel($x,$y)
                if($color.A -eq 0){continue}
                switch($theme.id){
                    'embers' {
                        $edge=63-80*$t+3*[math]::Sin($x*.38+$t*10)
                        if($y -lt $edge-4 -and $layer -ne "overlay"){ Pixel $b (18+$x) (16+$y) $color }
                        elseif($y -ge $edge-4 -and $y -lt $edge -and $layer -ne "mask"){
                            Pixel $b (18+$x) (16+$y) $palette[($x+$y)%4]
                        }
                    }
                    'dissolve' {
                        $edge=-5+85*$t+4*[math]::Sin($x*.61)
                        if($y -gt $edge+5){ Pixel $b (18+$x) (16+$y) $color }
                        elseif($y -gt $edge -and ($x+$y)%3 -ne 0){
                            Pixel $b (18+$x) (16+$y) $palette[($x+$y)%4]
                        }
                    }
                    'shards' {
                        $seam=21+3*[math]::Sin($y*.2)
                        $side=if($x -lt $seam){-1}else{1}
                        $lower=if($y -gt 31+4*[math]::Sin($x*.25)){1}else{0}
                        if($t -lt (.69+$lower*.09) -and [math]::Abs($x-$seam) -gt 1.3 -and [math]::Abs($y-31-4*[math]::Sin($x*.25)) -gt 1){
                            $dx=[int]($t*$side*(11+6*$lower))
                            $dy=[int](48*$t*$t-14*$t+8*$lower*$t)
                            Pixel $b (18+$x+$dx) (16+$y+$dy) $color
                        }
                    }
                }
            }
        }
    }
    if($layer -eq "mask"){return $b}
    for($i=0;$i -lt 44;$i++){
        $x=$rng.Next(17,63)
        $life=$rng.Next(25,69)/100.0
        $birth=$rng.Next(0,50)/100.0
        $jx=$rng.Next(-18,19)
        $speed=$rng.Next(15,46)
        $fragmentOffset=$rng.Next(-15,17)
        $age=$t-$birth
        if($age -lt 0 -or $age -gt $life -or $t -ge .97){continue}
        switch($theme.id){
            'embers' { $y=76-73*$birth-$age*$speed; $x+=$jx*$age }
            'dissolve' { $y=16+69*$birth-$age*$speed; $x+=$jx*$age*1.7 }
            'shards' { $y=37+50*$age*$age+$fragmentOffset; $x+=$jx*$age }
            'rune' { $x=40+($x-40)*(1.3-$age); $y=48+$jx*(1.5-$age) }
        }
        $ink=$palette[$(if($age -lt .17){3}elseif($age -lt .36){2}else{0})]
        Pixel $b ([int]$x) ([int]$y) $ink
        if($i%5 -eq 0 -and $age -lt .31){ Pixel $b ([int]$x+1) ([int]$y) $ink }
    }
    return $b
}
if($ExportEmbers){
    $out=Join-Path $asset 'sacrifice'
    New-Item -ItemType Directory -Force $out | Out-Null
    foreach($layer in @('mask','overlay')){
        $sheet=[Drawing.Bitmap]::new(640,282)
        $surface=[Drawing.Graphics]::FromImage($sheet)
        for($f=0;$f -lt 24;$f++){
            $frame=EffectsFrame $concepts[0] $f $layer
            if($layer -eq 'mask'){
                for($py=0;$py -lt 94;$py++){
                    for($px=0;$px -lt 80;$px++){
                        if($frame.GetPixel($px,$py).A -eq 255){$frame.SetPixel($px,$py,[Drawing.Color]::White)}
                    }
                }
            }
            if($f -eq 23){
                for($py=0;$py -lt 94;$py++){
                    for($px=0;$px -lt 80;$px++){
                        if($frame.GetPixel($px,$py).A -ne 0){throw "Nonempty final $layer frame"}
                    }
                }
            }
            $surface.DrawImageUnscaled($frame,(($f%8)*80),([math]::Floor($f/8)*94))
            $frame.Dispose()
        }
        $surface.Dispose()
        $sheet.Save((Join-Path $out "embers-$layer.png"),[Drawing.Imaging.ImageFormat]::Png)
        $sheet.Dispose()
    }
    $source=Join-Path $preview 'frames/frame-%02d.png'
    if(!(Test-Path (Join-Path $preview 'frames/frame-23.png'))){
        & $PSCommandPath
    }
    & ffmpeg -hide_banner -loglevel error -y -framerate 20 -i $source -vf 'crop=402:247:19:57,tpad=stop_mode=clone:stop_duration=0.55,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none' -loop 0 (Join-Path $out 'preview.gif')
    if($LASTEXITCODE -ne 0){throw 'GIF encoding failed.'}
    foreach($card in $cards.Values){$card.Dispose()}
    return
}
$frames=24
$boardFrames=Join-Path $preview 'frames'
New-Item -ItemType Directory -Force $boardFrames | Out-Null
$sheets=@{}
foreach($theme in $concepts){
    $sheets[$theme.id]=[Drawing.Bitmap]::new(80*8,94*3)
}
for($f=0;$f -lt $frames;$f++){
    $board=[Drawing.Bitmap]::new(856,590)
    $g=[Drawing.Graphics]::FromImage($board)
    $g.Clear([Drawing.ColorTranslator]::FromHtml('#171c29'))
    $g.InterpolationMode='NearestNeighbor'
    $g.PixelOffsetMode='Half'
    $g.TextRenderingHint='AntiAliasGridFit'
    Label 19 12 '나무 명판 · 카드 희생 이펙트' 26 '#ffe5bd' $true
    for($i=0;$i -lt 4;$i++){
        $theme=$concepts[$i]
        $x=19+($i%2)*415
        $y=57+[math]::Floor($i/2)*258
        Rect $x $y 402 247 '#242940'
        Rect $x $y 402 1 $theme.colors[2]
        Label ($x+13) ($y+9) $theme.title 19 '#ffe9ce' $true
        Label ($x+13) ($y+37) $theme.note 13 '#c4c2d3'
        $cardY=$y+95
        $g.DrawImage($cards.CardLightning,[Drawing.Rectangle]::new(($x+47),$cardY,88,128))
        $g.DrawImage($cards.CardIce,[Drawing.Rectangle]::new(($x+267),$cardY,88,128))
        $effect=EffectsFrame $theme $f
        $sheetSurface=[Drawing.Graphics]::FromImage($sheets[$theme.id])
        $sheetSurface.DrawImageUnscaled($effect,(($f%8)*80),([math]::Floor($f/8)*94))
        $sheetSurface.Dispose()
        $g.DrawImage($effect,[Drawing.Rectangle]::new(($x+121),($cardY-32),160,188))
        $effect.Dispose()
    }
    $g.Dispose()
    $board.Save((Join-Path $boardFrames ('frame-{0:D2}.png' -f $f)),[Drawing.Imaging.ImageFormat]::Png)
    if($f -eq 11){ $board.Save((Join-Path $PSScriptRoot 'comparison.png'),[Drawing.Imaging.ImageFormat]::Png) }
    $board.Dispose()
}
foreach($key in $sheets.Keys){
    $sheets[$key].Save((Join-Path $PSScriptRoot "$key.png"),[Drawing.Imaging.ImageFormat]::Png)
    $sheets[$key].Dispose()
}
foreach($card in $cards.Values){$card.Dispose()}
& ffmpeg -hide_banner -loglevel error -y -framerate 20 -i (Join-Path $boardFrames 'frame-%02d.png') -vf 'tpad=stop_mode=clone:stop_duration=0.55,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none' -loop 0 (Join-Path $PSScriptRoot 'comparison.gif')
if($LASTEXITCODE -ne 0){throw 'GIF encoding failed.'}


