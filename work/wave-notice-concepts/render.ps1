$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$asset=Join-Path $PSScriptRoot '../../exports/v1/spells-to-go-ui/package/Assets/SpellsToGo/UI/Sprites'
$paper=[Drawing.Bitmap]::new((Join-Path $asset 'NoticeParchment.png'))
$button=[Drawing.Bitmap]::new((Join-Path $asset 'button-normal.png'))
function Canvas($w,$h){ [Drawing.Bitmap]::new($w,$h) }
function Surface($b){
    $surface=[Drawing.Graphics]::FromImage($b)
    $surface.Clear([Drawing.ColorTranslator]::FromHtml('#171c2a'))
    $surface.InterpolationMode='NearestNeighbor'
    $surface.PixelOffsetMode='Half'
    $surface.TextRenderingHint='AntiAliasGridFit'
    return $surface
}
function Slice($src,$x,$y,$w,$h){
    $dx=@(0,24,($w-24),$w); $dy=@(0,24,($h-24),$h)
    for($r=0;$r -lt 3;$r++){
        for($c=0;$c -lt 3;$c++){
            $d=[Drawing.Rectangle]::new(($x+$dx[$c]),($y+$dy[$r]),($dx[$c+1]-$dx[$c]),($dy[$r+1]-$dy[$r]))
            $g.DrawImage($src,$d,($c*12),($r*12),12,12,[Drawing.GraphicsUnit]::Pixel)
        }
    }
}
function Center($x,$y,$value,$size,$ink){
    $font=[Drawing.Font]::new('Malgun Gothic',$size,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
    $brush=Brush $ink
    $fmt=[Drawing.StringFormat]::new()
    $fmt.Alignment='Center'
    $g.DrawString($value,$font,$brush,[single]$x,[single]$y,$fmt)
    $font.Dispose(); $brush.Dispose(); $fmt.Dispose()
}
function Diamond($x,$y,$r,$color){
    Poly @($x,($y-$r),($x+$r),$y,$x,($y+$r),($x-$r),$y) $color
}
function Mark($x,$y,$good,$color){
    if($good){
        Poly @(($x-10),$y,($x-3),($y+6),($x+9),($y-8),($x+12),($y-5),($x-3),($y+12),($x-13),($y+3)) $color
    }else{
        Rect ($x-2) ($y-10) 4 14 $color
        Rect ($x-2) ($y+7) 4 4 $color
    }
}
$result=Canvas 868 823
$g=Surface $result
Label 21 14 '스테이지 결과 · 나무틀 양피지' 26 '#ffe9d0' $true
$styles=@('인장형','결과 요약형','전장 표지형')
for($i=0;$i -lt 3;$i++){
    $row=64+247*$i
    Label 22 $row $styles[$i] 16 '#d9b990' $true
    for($side=0;$side -lt 2;$side++){
        $win=$side -eq 0
        $x=22+$side*420
        $y=$row+28
        $deep=if($win){'#315e4b'}else{'#803f44'}
        $bright=if($win){'#d4efb1'}else{'#ffcab0'}
        $heading=if($win){'스테이지 클리어'}else{'패배'}
        Slice $paper $x $y 403 211
        switch($i){
            0 {
                Diamond ($x+202) ($y+32) 22 $deep
                Mark ($x+202) ($y+31) $win $bright
            }
            1 {
                Rect ($x+39) ($y+42) 325 1 $deep
                Rect ($x+39) ($y+124) 325 1 $deep
                Diamond ($x+201) ($y+42) 6 $deep
            }
            2 {
                Rect ($x+18) ($y+18) 367 50 $deep
                Mark ($x+59) ($y+42) $win $bright
            }
        }
        if($i -eq 2){Center ($x+207) ($y+26) $heading 25 $bright}
        else{Center ($x+202) ($y+53) $heading 25 $deep}
        $line=if($i -eq 1){
            if($win){'완료한 웨이브  5 / 5'}else{'완료한 웨이브  3 / 5'}
        }elseif($win){'초원 · 모든 웨이브를 막아냈어요.'}else{'초원 · 웨이브 4에서 방어선이 무너졌어요.'}
        Center ($x+202) ($y+93) $line 16 '#543836'
        Slice $button ($x+139) ($y+137) 125 50
        Center ($x+202) ($y+151) '확인' 16 '#281f26'
    }
}
$g.Dispose(); $result.Save((Join-Path $PSScriptRoot 'stage-results.png'),[Drawing.Imaging.ImageFormat]::Png); $result.Dispose()

function MotionCard($x,$y,$good,$style,$tick){
    $accent=if($good){'#69edb5'}else{'#ff815f'}
    $dim=if($good){'#284a46'}else{'#592d3c'}
    $deep=if($good){'#183534'}else{'#401e2e'}
    $category=if($good){'버프 · 목표 일치'}else{'패널티 · 목표 초과'}
    $effect=if($good){'세 주문 강화'}else{'첫 시전 2초 지연'}
    Poly @(($x+6),$y,($x+388),$y,($x+394),($y+6),($x+394),($y+79),($x+388),($y+85),($x+6),($y+85),$x,($y+79),$x,($y+6)) $accent
    Rect ($x+4) ($y+4) 386 77 $deep
    Rect ($x+8) ($y+8) 57 69 $dim
    Mark ($x+36) ($y+41) $good $accent
    Label ($x+83) ($y+10) $category 15 $accent $true
    Label ($x+81) ($y+32) $effect 25 '#fff2dc' $true
    if($tick -lt 11 -or $tick -gt 46){
        for($k=0;$k -lt 8;$k++){
            $spark=($k*37+$tick*10)%101
            $px=if($good){$x+$spark}else{$x+389-$spark}
            $py=if($good){$y-3-($k*13+$tick*3)%11}else{$y+85+($k*11+$tick*2)%12}
            if($good){Diamond $px $py (1+$k%2) $accent}
            else{Rect $px $py 5 2 $accent}
        }
    }
    if($style -eq 2 -and $tick -gt 46){
        $rng=[Random]::new(390)
        for($k=0;$k -lt 43;$k++){
            $px=$x+$rng.Next(0,394); $py=$y+$rng.Next(0,85)
            if($px-$x -lt ($tick-47)*29){Rect $px $py (5+$k%9) (3+$k%4) '#20263a'}
        }
    }
}
$names=@('측면 스윕','스탬프','픽셀 소거')
$motion=@('반대 방향에서 진입하고 그대로 빠져나감','중앙에서 커지며 찍히고 작아지며 퇴장','왼쪽에서 미끄러져 들어오고 픽셀로 소거')
for($tick=0;$tick -lt 66;$tick++){
    $board=Canvas 868 587
    $g=Surface $board
    Label 21 13 '웨이브 효과 · 등장과 퇴장' 26 '#ffe9d0' $true
    for($i=0;$i -lt 3;$i++){
        $row=65+169*$i
        Label 22 $row $names[$i] 17 '#f2d4ac' $true
        Label 143 ($row+3) $motion[$i] 14 '#c6c3d5'
        for($side=0;$side -lt 2;$side++){
            $good=$side -eq 0
            $left=22+$side*420
            Rect $left ($row+31) 403 112 '#20263a'
            if($tick -ge 61){continue}
            $saved=$g.Save()
            $g.SetClip([Drawing.Rectangle]::new($left,($row+31),403,112))
            $x=$left+5; $y=$row+44
            $sign=if($good){-1}else{1}
            if($i -eq 0){
                if($tick -lt 10){
                    $x+=$sign*[int](400*[math]::Pow((1-$tick/10.0),3))
                }elseif($tick -gt 47){
                    $x-=$sign*[int](405*[math]::Pow((($tick-47)/13.0),2))
                }
                MotionCard $x $y $good $i $tick
            }elseif($i -eq 1){
                $scale=if($tick -lt 9){[math]::Min(1.08,.55+$tick*.065)}elseif($tick -gt 47){[math]::Max(.06,1-($tick-47)*.074)}else{1}
                $stamp=Canvas 420 112
                $parent=$g
                $g=[Drawing.Graphics]::FromImage($stamp)
                $g.TextRenderingHint='AntiAliasGridFit'
                MotionCard 13 13 $good $i $tick
                $g.Dispose()
                $g=$parent
                $w=[int](420*$scale)
                $h=[int](112*$scale)
                $g.DrawImage($stamp,[Drawing.Rectangle]::new(($x+197-[int]($w/2)),($y+43-[int]($h/2)),$w,$h))
                $stamp.Dispose()
            }else{
                if($tick -lt 10){$x-=[int](105*[math]::Pow((1-$tick/10.0),2))}
                MotionCard $x $y $good $i $tick
                if($tick -gt 47){
                    $wipe=($tick-47)*31
                    Rect $x ($y-10) $wipe 104 '#20263a'
                    for($k=0;$k -lt 12;$k++){
                        $px=$x+$wipe+(($k*53+$tick*9)%39)-16
                        $py=$y+($k*17+$tick*2)%85
                        Rect $px $py (2+$k%5) (2+$k%3) $(if($good){'#69edb5'}else{'#ff815f'})
                    }
                }
            }
            $g.Restore($saved)
        }
    }
    $g.Dispose()
    if($tick -eq 26){$board.Save((Join-Path $PSScriptRoot 'wave-effects.png'),[Drawing.Imaging.ImageFormat]::Png)}
    $board.Save((Join-Path $PSScriptRoot ('review/frame-{0:D2}.png' -f $tick)),[Drawing.Imaging.ImageFormat]::Png)
    $board.Dispose()
}
$paper.Dispose(); $button.Dispose()
& ffmpeg -hide_banner -loglevel error -y -framerate 20 -i (Join-Path $PSScriptRoot 'review/frame-%02d.png') -vf 'split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=none' -loop 0 (Join-Path $PSScriptRoot 'wave-effects.gif')
if($LASTEXITCODE -ne 0){throw 'GIF encoding failed'}



