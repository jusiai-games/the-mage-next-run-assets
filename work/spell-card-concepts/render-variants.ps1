param([switch]$DefinitionsOnly)
Add-Type -AssemblyName System.Drawing
function Brush($hex) { [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($hex)) }
function Rect($x,$y,$w,$h,$c) {
    $b=Brush $c
    $g.FillRectangle($b,[int]$x,[int]$y,[int]$w,[int]$h)
    $b.Dispose()
}
function Poly($coords,$c) {
    [Drawing.Point[]]$points = for($i=0;$i -lt $coords.Count;$i+=2){
        [Drawing.Point]::new($coords[$i],$coords[$i+1])
    }
    $b=Brush $c
    $g.FillPolygon($b,$points)
    $b.Dispose()
}
function Label($x,$y,$s,$size,$c,$bold=$false) {
    $style=if($bold){[Drawing.FontStyle]::Bold}else{[Drawing.FontStyle]::Regular}
    $f=[Drawing.Font]::new('Malgun Gothic',$size,$style,[Drawing.GraphicsUnit]::Pixel)
    $b=Brush $c
    $g.DrawString($s,$f,$b,[single]$x,[single]$y)
    $b.Dispose()
    $f.Dispose()
}
function Frame($inset,$color) {
    $l=$inset; $r=44-$inset; $b=64-$inset; $k=3
    Poly @(($l+$k),$l,($r-$k),$l,$r,($l+$k),$r,($b-$k),($r-$k),$b,($l+$k),$b,$l,($b-$k),$l,($l+$k)) $color
}
function Icon($id,$mid,$light){
    switch($id){
        0 {
            Poly @(10,25,14,19,17,20,19,14,23,17,28,11,27,17,32,16,30,22,26,27,19,30,14,29) $mid
            Poly @(14,25,20,21,24,21,27,17,26,23,22,26,16,28) $light
        }
        1 {
            Poly @(23,10,31,10,25,19,32,19,17,32,20,23,12,23) $mid
            Poly @(24,11,28,11,22,21,27,21,19,28,22,21,16,21) $light
        }
        2 {
            Poly @(22,9,25,17,33,20,25,23,22,32,19,24,11,20,19,17) $mid
            Poly @(22,14,24,19,28,20,24,22,22,27,20,22,16,20,20,19) $light
        }
        3 {
            Poly @(12,29,16,18,29,10,32,13,26,25,17,30) $mid
            Poly @(12,29,20,18,29,11,25,21,18,27) $light
        }
        4 {
            Poly @(9,17,17,12,29,12,34,17,30,22,22,22,26,24,23,29,15,29,20,26,18,24,10,24,15,20,28,19,29,16,20,15) $mid
            Poly @(12,17,19,13,29,13,32,16,27,15,19,15,15,18) $light
        }
    }
}
$styles=@(
    @{name='나무 명판'; note='나뭇결과 회청색 조약돌'; outer='#775344'; edge='#b88861'; paper='#eacda1'; ink='#3e2c31'},
    @{name='원소 유리창'; note='색유리 조각과 짙은 이름 띠'; outer='#45546d'; edge='#839db3'; paper='#e8e3d8'; ink='#222d43'},
    @{name='양피지 기록'; note='필사본 삽화와 넓은 설명란'; outer='#c5a477'; edge='#f3d5a3'; paper='#f3d5a3'; ink='#4b3540'},
    @{name='룬 인장'; note='남색 카드지와 원형 마법진'; outer='#45415b'; edge='#aa91ac'; paper='#303049'; ink='#eee2f1'}
)
$spells=@(
    @{name='화염탄'; type='강화'; effect='피해 증가'; deep='#703833'; mid='#ee7547'; light='#ffda83'},
    @{name='연쇄 번개'; type='신규'; effect='두 마리 타격'; deep='#274969'; mid='#73b8e2'; light='#e2f9ff'},
    @{name='마력 폭발'; type='신규'; effect='별 그리기'; deep='#583a70'; mid='#bb82dc'; light='#f7dafa'}
)
function CardFace($i,$j,$p) {
        $s=$styles[$i]
        $surface=$g
        $card=[Drawing.Bitmap]::new(44,64)
        $g=[Drawing.Graphics]::FromImage($card)
        Frame 0 '#111321'
        Frame 1 $s.outer
        Frame 2 $s.edge
        Frame 3 $s.paper
        Rect 4 5 36 32 $p.deep
        switch($i){
            0 {
                Rect 6 7 32 28 '#483645'
                foreach($yy in @(9,16,23,30)){Rect 6 $yy 32 1 '#594450'}
                foreach($xx in @(4,37)){foreach($yy in @(5,34)){Rect $xx $yy 3 3 '#91a6aa'}}
            }
            1 {
                Poly @(5,6,20,6,15,19,5,24) $p.mid
                Poly @(39,6,23,6,28,18,39,12) '#35435a'
                Poly @(5,28,17,21,23,35,5,35) '#222a43'
                Poly @(39,14,29,20,25,35,39,35) $p.mid
            }
            2 {
                Rect 5 6 34 29 '#dab789'
                Rect 7 8 30 25 '#e9c99b'
                foreach($xx in @(9,14,29,34)){Rect $xx 11 1 18 '#e0bd90'}
            }
            3 {
                $pen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml($p.mid))
                $g.DrawEllipse($pen,8,7,27,27)
                $g.DrawEllipse($pen,11,10,21,21)
                $pen.Dispose()
                foreach($point in @(@(21,6),@(8,20),@(34,20),@(21,33))){
                    Rect $point[0] $point[1] 2 2 $p.light
                }
            }
        }
        Icon $j $p.mid $(if($i -eq 2){$p.deep}else{$p.light})
        Rect 4 37 36 8 $(if($i -eq 2){$s.paper}else{$p.deep})
        Rect 6 45 32 1 $s.edge
        $g.Dispose()
        $g=$surface
        return $card
}
if ($DefinitionsOnly) { return }
$board=[Drawing.Bitmap]::new(1060,760)
$boardGraphics=[Drawing.Graphics]::FromImage($board)
$g=$boardGraphics
$g.TextRenderingHint='AntiAliasGridFit'
$g.Clear([Drawing.ColorTranslator]::FromHtml('#141825'))
Label 32 22 '주문 넣고 갑니다' 15 '#e0b984' $true
Label 30 47 '주문 카드 디자인 시안' 34 '#fff2df' $true
Label 32 98 '화염탄 · 연쇄 번개 · 마력 폭발' 15 '#b4bcd3'
for($i=0;$i -lt $styles.Count;$i++){
    $s=$styles[$i]
    $x=30+($i%2)*506
    $y=139+[math]::Floor($i/2)*306
    Rect $x $y 494 292 '#212838'
    Rect $x $y 494 1 $s.edge
    Label ($x+27) ($y+13) $s.name 23 '#fff2df' $true
    Label ($x+28) ($y+47) $s.note 14 '#b4bcd3'
    for($j=0;$j -lt $spells.Count;$j++){
        $p=$spells[$j]
        $card=CardFace $i $j $p
        $cx=$x+29+$j*151
        $cy=$y+77
        $g.InterpolationMode='NearestNeighbor'
        $g.PixelOffsetMode='Half'
        $g.DrawImage($card,[Drawing.Rectangle]::new($cx,$cy,132,192))
        $card.Dispose()
        $title=if($i -eq 2){$s.ink}else{'#fff2df'}
        Label ($cx+15) ($cy+112) $p.name 15 $title $true
        Label ($cx+16) ($cy+143) $p.type 11 $s.ink $true
        Label ($cx+16) ($cy+157) $p.effect 12 $s.ink
    }
}
$g.Dispose()
$path=Join-Path $PSScriptRoot 'spell-card-variants.png'
$board.Save($path,[Drawing.Imaging.ImageFormat]::Png)
$board.Dispose()

