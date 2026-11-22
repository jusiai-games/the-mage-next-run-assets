$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$out=Join-Path $PSScriptRoot '../../exports/v1/spells-to-go-ui/package/Assets/SpellsToGo/UI/Sprites'
$asset=[Drawing.Bitmap]::new(36,36)
$g=[Drawing.Graphics]::FromImage($asset)
Poly @(5,0,31,0,36,5,36,31,31,36,5,36,0,31,0,5) '#1b1b2a'
Poly @(6,1,30,1,35,6,35,30,30,35,6,35,1,30,1,6) '#ac7d56'
Rect 4 4 28 28 '#594139'
Rect 10 4 16 28 '#bd936d'
Rect 11 5 14 26 '#e9cba2'
Rect 11 5 14 1 '#f6dfb7'
Rect 11 30 14 1 '#c59a72'
foreach($x in 2,26){
    Rect $x 6 8 24 '#684537'
    Rect ($x+1) 6 6 24 '#936547'
    Rect ($x+1) 7 1 22 '#bc8960'
    Rect ($x+6) 7 1 22 '#674536'
    foreach($y in 6,26){
        Rect ($x+2) $y 5 4 '#465560'
        Rect ($x+3) $y 3 2 '#92a5a6'
    }
}
$g.Dispose()
$asset.Save((Join-Path $out 'NoticeParchment.png'),[Drawing.Imaging.ImageFormat]::Png)
$board=[Drawing.Bitmap]::new(824,541)
$g=[Drawing.Graphics]::FromImage($board)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#171b2a'))
$g.InterpolationMode='NearestNeighbor'
$g.PixelOffsetMode='Half'
$g.TextRenderingHint='AntiAliasGridFit'
function Parchment($x,$y,$w,$h){
    $dx=@(0,24,($w-24),$w)
    $dy=@(0,24,($h-24),$h)
    for($r=0;$r -lt 3;$r++){
        for($c=0;$c -lt 3;$c++){
            $dest=[Drawing.Rectangle]::new(($x+$dx[$c]),($y+$dy[$r]),($dx[$c+1]-$dx[$c]),($dy[$r+1]-$dy[$r]))
            $g.DrawImage($asset,$dest,($c*12),($r*12),12,12,[Drawing.GraphicsUnit]::Pixel)
        }
    }
}
function CenterNotice($x,$y,$w,$height,$value,$size,$bold=$false){
    $style=if($bold){[Drawing.FontStyle]::Bold}else{[Drawing.FontStyle]::Regular}
    $f=[Drawing.Font]::new('Malgun Gothic',$size,$style,[Drawing.GraphicsUnit]::Pixel)
    $ink=Brush '#4f3333'
    $fmt=[Drawing.StringFormat]::new()
    $fmt.Alignment='Center'
    $fmt.LineAlignment='Center'
    $g.DrawString($value,$f,$ink,[Drawing.RectangleF]::new($x,$y,$w,$height),$fmt)
    $f.Dispose(); $ink.Dispose(); $fmt.Dispose()
}
Label 24 20 '나무틀 양피지 · 높이별 안내' 26 '#ffe9cf' $true
Label 25 76 '한 줄 · 웨이브 예고' 15 '#e5c094' $true
Parchment 25 106 774 64
CenterNotice 45 106 734 64 '목표 9 · 적 6마리 (근거리 4 · 원거리 2)' 20
Label 25 189 '두 줄 · 카드 선택 안내' 15 '#e5c094' $true
Parchment 25 219 774 93
CenterNotice 45 234 734 27 '숫자를 바꿀 카드를 고르세요' 20 $true
CenterNotice 45 263 734 26 '손패 또는 장착 슬롯에서 카드 한 장을 선택하세요.' 17
Label 25 339 '여러 줄 · 희생 확인' 15 '#e5c094' $true
Parchment 25 369 774 144
CenterNotice 45 387 734 29 '화염구를 희생할까요?' 21 $true
CenterNotice 45 421 734 23 '화염구 4 · 이번 스테이지 동안 덱에서 빠집니다.' 17
CenterNotice 45 446 734 23 '남은 웨이브 3 · 덱 18장에서 17장으로 감소' 17
CenterNotice 45 471 734 22 '희생은 되돌릴 수 없습니다.' 16
$g.Dispose()
$board.Save((Join-Path $PSScriptRoot 'wood-parchment-heights.png'),[Drawing.Imaging.ImageFormat]::Png)
$board.Dispose(); $asset.Dispose()



