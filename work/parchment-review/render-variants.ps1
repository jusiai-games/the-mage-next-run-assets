$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$board=[Drawing.Bitmap]::new(780,496)
$g=[Drawing.Graphics]::FromImage($board)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#171b2a'))
$g.InterpolationMode='NearestNeighbor'
$g.PixelOffsetMode='Half'
$g.TextRenderingHint='AntiAliasGridFit'
function MidText($x,$y,$value,$size,$ink,$bold){
    $style=if($bold){[Drawing.FontStyle]::Bold}else{[Drawing.FontStyle]::Regular}
    $font=[Drawing.Font]::new('Malgun Gothic',$size,$style,[Drawing.GraphicsUnit]::Pixel)
    $brush=Brush $ink
    $fmt=[Drawing.StringFormat]::new()
    $fmt.Alignment='Center'
    $g.DrawString($value,$font,$brush,[single]$x,[single]$y,$fmt)
    $font.Dispose(); $brush.Dispose(); $fmt.Dispose()
}
Label 26 15 '웨이브 안내 양피지 · 디자인 시안' 25 '#ffe9cf' $true
$names=@('말린 양피지','나무틀 양피지','봉인된 양피지')
for($i=0;$i -lt 3;$i++){
    $row=65+141*$i
    Rect 24 $row 732 128 '#252a3e'
    Label 42 ($row+9) $names[$i] 17 '#f2d6af' $true
    $art=[Drawing.Bitmap]::new(246,38)
    $surface=$g
    $g=[Drawing.Graphics]::FromImage($art)
    switch($i){
        0 {
            Poly @(3,6,12,6,15,8,230,8,235,5,243,5,246,9,246,29,243,33,235,33,230,30,15,30,12,34,3,34,0,30,0,10) '#31222c'
            Rect 11 9 223 21 '#aa704f'
            Rect 15 10 216 19 '#f2d4a5'
            Rect 18 11 210 1 '#ffe7bf'
            Rect 18 27 210 1 '#d89c71'
            foreach($x in 2,234){
                Rect $x 8 10 24 '#935e43'
                Rect ($x+1) 9 8 20 '#cd9363'
                Rect ($x+2) 11 3 16 '#f4c58a'
                Rect ($x+3) 29 6 2 '#684337'
            }
        }
        1 {
            Poly @(5,6,241,6,246,11,246,28,241,33,5,33,0,28,0,11) '#1b1b2a'
            Poly @(6,7,240,7,245,12,245,27,240,32,6,32,1,27,1,12) '#ac7d56'
            Rect 4 10 238 19 '#594139'
            Rect 10 10 226 19 '#bd936d'
            Rect 12 11 222 17 '#e9cba2'
            Rect 15 12 216 1 '#f6dfb7'
            foreach($x in 4,237){
                foreach($y in 11,24){
                    Rect $x $y 5 4 '#465560'
                    Rect ($x+1) $y 3 2 '#92a5a6'
                }
            }
        }
        2 {
            Poly @(5,7,21,7,24,8,240,8,245,12,243,15,246,20,242,24,246,29,241,33,5,32,0,27,2,22,0,16) '#5f3b3a'
            Poly @(6,9,237,9,243,12,240,16,244,20,240,25,243,29,239,31,6,30,2,26,4,22,2,16) '#e6c092'
            Rect 21 11 212 17 '#f3d3a6'
            Rect 24 11 206 1 '#ffebc7'
            Rect 24 27 205 1 '#bd8b65'
            Poly @(12,9,19,12,20,20,15,26,7,24,4,17,7,11) '#653747'
            Poly @(12,10,17,13,18,19,13,23,8,22,6,17,8,12) '#a65356'
            Poly @(12,12,15,16,12,20,9,16) '#f0ad83'
        }
    }
    $g.Dispose()
    $g=$surface
    $g.DrawImage($art,[Drawing.Rectangle]::new(43,($row+40),492,76))
    $art.Dispose()
    MidText $(if($i -eq 2){305}else{289}) ($row+65) '목표 9 · 적 6마리 (근거리 4 · 원거리 2)' 19 '#4f3333' $true
    Label 556 ($row+56) (@('둥근 말림과 밝은 종이','나무 테두리와 조약돌','붉은 밀랍 인장과')[$i]) 14 '#d4c3bb'
    if($i -eq 2){Label 556 ($row+77) '고르지 않은 종이 끝' 14 '#d4c3bb'}
}
$g.Dispose()
$board.Save((Join-Path $PSScriptRoot 'forecast-variants.png'),[Drawing.Imaging.ImageFormat]::Png)
$board.Dispose()

