$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'render-variants.ps1') -DefinitionsOnly

$sceneArt=Join-Path $PSScriptRoot '../../exports/v1/meadow-wave-mobile'
$cards=@(
    @{name='화염구'; number='4'; icon=0; deep='#703833'; mid='#ee7547'; light='#ffda83'},
    @{name='연쇄 번개'; number='3'; icon=1; deep='#274969'; mid='#73b8e2'; light='#e2f9ff'},
    @{name='불씨'; number='1'; icon=0; deep='#703833'; mid='#ee7547'; light='#ffda83'},
    @{name='돌풍'; number='2'; icon=4; deep='#424b37'; mid='#aec785'; light='#f3ebad'},
    @{name='얼음 방패'; number='2'; icon=3; deep='#305c5e'; mid='#78cbbd'; light='#d5fff2'}
)
function ImageLayer($name,$x,$y){
    $art=[Drawing.Bitmap]::new((Join-Path $sceneArt $name))
    $g.DrawImage($art,[Drawing.Rectangle]::new($x,$y,[int]($art.Width*2.25),[int]($art.Height*2.25)))
    $art.Dispose()
}
function Panel($x,$y,$w,$h){
    Rect $x $y $w $h '#1c1d29'
    Rect ($x+1) ($y+1) ($w-2) ($h-2) '#816449'
    Rect ($x+3) ($y+3) ($w-6) ($h-6) '#302833'
}
function Center($x,$y,$message,$size,$ink,$bold=$false){
    $style=if($bold){[Drawing.FontStyle]::Bold}else{[Drawing.FontStyle]::Regular}
    $font=[Drawing.Font]::new('Malgun Gothic',$size,$style,[Drawing.GraphicsUnit]::Pixel)
    $brush=Brush $ink
    $align=[Drawing.StringFormat]::new()
    $align.Alignment='Center'
    $g.DrawString($message,$font,$brush,[single]$x,[single]$y,$align)
    $align.Dispose()
    $brush.Dispose()
    $font.Dispose()
}
function PlaceCard($index,$p,$cx,$cy,$flash=$false){
    $theme=$styles[$index]
    if($flash){Rect ($cx-2) ($cy-2) 64 84 '#ffe5a2'}
    $card=CardFace $index $p.icon $p
    $g.DrawImage($card,[Drawing.Rectangle]::new($cx,$cy,60,80))
    $card.Dispose()
    $title=if($index -eq 2){$theme.ink}else{'#fff2df'}
    Center ($cx+30) ($cy+46) $p.name 10 $title $true
    Center ($cx+30) ($cy+57) $p.number 15 $theme.ink $true
}
function DrawEnemy($x,$y){
    Poly @($x,($y+8),($x+3),($y+2),($x+10),$y,($x+18),$y,($x+22),($y+4),($x+25),($y+11),($x+22),($y+16),($x+4),($y+16)) '#344b4b'
    Rect ($x+4) ($y+5) 17 8 '#629480'
    Rect ($x+7) ($y+4) 10 3 '#96b392'
    Rect ($x+6) ($y+9) 3 4 '#263e44'
    Rect ($x+13) ($y+9) 3 4 '#263e44'
}
function Screen($index,$planning){
    $screen=[Drawing.Bitmap]::new(360,780)
    $g=[Drawing.Graphics]::FromImage($screen)
    $g.InterpolationMode='NearestNeighbor'
    $g.PixelOffsetMode='Half'
    $g.TextRenderingHint='AntiAliasGridFit'
    ImageLayer 'distant-meadow.png' 0 0
    ImageLayer 'meadow-terrain.png' 0 180
    ImageLayer 'meadow-hedge.png' 0 149
    ImageLayer 'spell-panel.png' 0 504
    ImageLayer 'wizard-idle.png' 18 281
    if($planning -ne 0){
        $dim=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(91,15,17,30))
        $g.FillRectangle($dim,0,0,360,780)
        $dim.Dispose()
        Panel 17 23 326 67
        Center 180 32 '웨이브 준비' 18 '#ffe5bd' $true
        Center 180 57 '목표 9 · 적 6마리 (근거리)' 12 '#f1d4b2'
        Center 180 469 '장착 슬롯' 13 '#ffe4bd' $true
        for($j=0;$j -lt 3;$j++){
            $x=@(77,150,223)[$j]
            Panel ($x-2) 508 64 84
            if($planning -eq 2){
                PlaceCard $index $cards[@(0,1,4)[$j]] $x 510
            }else{
                Center ($x+30) 541 '빈 슬롯' 11 '#a38e88'
            }
        }
        $sum=if($planning -eq 2){'9 / 9 일치'}else{'0 / 9 미달'}
        Center 180 599 $sum 15 '#f8db90' $true
        Center 180 626 '손패' 13 '#ffe4bd' $true
        for($j=0;$j -lt 5;$j++){
            if($planning -eq 1 -or $j -in 2,3){
                PlaceCard $index $cards[$j] (17+$j*67) 650
            }
        }
        Panel 17 738 100 33
        Center 67 743 '희생' 14 '#f7dbbc' $true
        Panel 186 738 157 33
        Center 264 742 '전투 시작' 15 $(if($planning -eq 2){'#ffe6bc'}else{'#99877f'}) $true
    }else{
        Panel 17 23 326 57
        Center 180 30 '웨이브 1' 16 '#ffe5bd' $true
        Center 180 53 '일치! 세 주문 강화' 12 '#f1d4b2'
        DrawEnemy 250 329
        DrawEnemy 289 310
        DrawEnemy 323 335
        Rect 13 502 334 2 '#b28a5d'
        Center 180 546 '방벽' 12 '#ffe4bd' $true
        Rect 66 565 228 8 '#221f2b'
        Rect 68 567 143 4 '#80c0ad'
        for($j=0;$j -lt 3;$j++){
            $x=@(63,150,237)[$j]
            Center ($x+30) 627 '강화' 11 '#ffe4ad' $true
            PlaceCard $index $cards[@(0,1,4)[$j]] $x 643 ($j -eq 0)
            if($j -lt 2){
                Rect $x 729 60 7 '#201c26'
                Rect ($x+2) 731 @(12,37)[$j] 3 '#9acaaf'
            }
        }
    }
    $g.Dispose()
    return $screen
}
function RenderComparison($planning,$heading,$filename){
    $board=[Drawing.Bitmap]::new(1552,897)
    $g=[Drawing.Graphics]::FromImage($board)
    $g.Clear([Drawing.ColorTranslator]::FromHtml('#141825'))
    $g.TextRenderingHint='AntiAliasGridFit'
    Label 24 13 $heading 27 '#fff2df' $true
    for($i=0;$i -lt $styles.Count;$i++){
        $x=20+$i*384
        Label $x 62 $styles[$i].name 19 '#ffe5bd' $true
        $screen=Screen $i $planning
        $g.DrawImageUnscaled($screen,$x,102)
        $screen.Dispose()
    }
    $g.Dispose()
    $board.Save((Join-Path $PSScriptRoot $filename),[Drawing.Imaging.ImageFormat]::Png)
    $board.Dispose()
}
RenderComparison 1 '웨이브 준비 · 손패 5장과 빈 슬롯' 'spell-card-hand-comparison.png'
RenderComparison 2 '웨이브 준비 · 장착 완료와 남은 손패' 'spell-card-planning-comparison.png'
RenderComparison 0 '전투 · 스킬 슬롯과 충전 표시' 'spell-card-combat-comparison.png'


