$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'render-variants.ps1') -DefinitionsOnly

$out=Join-Path $PSScriptRoot '../../exports/v1/wood-spell-cards'
New-Item -ItemType Directory -Path $out -Force | Out-Null
$elements=@(
    @{file='CardFire'; icon=0; deep='#703833'; mid='#ee7547'; light='#ffda83'},
    @{file='CardLightning'; icon=1; deep='#274969'; mid='#73b8e2'; light='#e2f9ff'},
    @{file='CardIce'; icon=3; deep='#305c5e'; mid='#78cbbd'; light='#d5fff2'},
    @{file='CardWind'; icon=4; deep='#424b37'; mid='#aec785'; light='#f3ebad'}
)
function SaveSprite($bitmap,$name,$width,$height){
    if($bitmap.Width -ne $width -or $bitmap.Height -ne $height){
        throw "Unexpected dimensions for $name"
    }
    $visible=0
    for($y=0;$y -lt $height;$y++){
        for($x=0;$x -lt $width;$x++){
            $alpha=$bitmap.GetPixel($x,$y).A
            if($alpha -notin 0,255){ throw "Partial alpha in $name at ($x,$y)" }
            if($alpha -eq 255){ $visible++ }
        }
    }
    if($visible -eq 0){ throw "Empty sprite: $name" }
    $bitmap.Save((Join-Path $out "$name.png"),[Drawing.Imaging.ImageFormat]::Png)
    $bitmap.Dispose()
}
foreach($element in $elements){
    $face=CardFace 0 $element.icon $element
    SaveSprite $face $element.file 44 64
}
$empty=[Drawing.Bitmap]::new(44,64)
$g=[Drawing.Graphics]::FromImage($empty)
Frame 0 '#111321'
Frame 1 '#775344'
Frame 2 '#927255'
Frame 3 '#302833'
Rect 6 6 32 52 '#3a2d36'
foreach($y in @(9,17,25,33,41,49,57)){ Rect 6 $y 32 1 '#43343b' }
foreach($x in @(4,37)){ foreach($y in @(5,56)){ Rect $x $y 3 3 '#667b85' } }
$g.Dispose()
SaveSprite $empty 'SlotEmpty' 44 64

$flash=[Drawing.Bitmap]::new(44,64)
$g=[Drawing.Graphics]::FromImage($flash)
Frame 0 '#ffe5a2'
$g.CompositingMode='SourceCopy'
$clear=[Drawing.SolidBrush]::new([Drawing.Color]::Transparent)
$g.FillPolygon($clear,[Drawing.Point[]]@(
    [Drawing.Point]::new(5,2),[Drawing.Point]::new(39,2),[Drawing.Point]::new(42,5),
    [Drawing.Point]::new(42,59),[Drawing.Point]::new(39,62),[Drawing.Point]::new(5,62),
    [Drawing.Point]::new(2,59),[Drawing.Point]::new(2,5)
))
$clear.Dispose()
$g.Dispose()
SaveSprite $flash 'SlotFlash' 44 64

$track=[Drawing.Bitmap]::new(44,5)
$g=[Drawing.Graphics]::FromImage($track)
Rect 0 0 44 5 '#201c26'
Rect 1 1 42 3 '#594450'
$g.Dispose()
SaveSprite $track 'ChargeTrack' 44 5

$fill=[Drawing.Bitmap]::new(42,3)
$g=[Drawing.Graphics]::FromImage($fill)
Rect 0 0 42 3 '#9acaaf'
Rect 0 0 42 1 '#c2e3c5'
$g.Dispose()
SaveSprite $fill 'ChargeFill' 42 3

function CenterLabel($center,$y,$message,$size,$ink,$bold=$false){
    $style=if($bold){[Drawing.FontStyle]::Bold}else{[Drawing.FontStyle]::Regular}
    $font=[Drawing.Font]::new('Malgun Gothic',$size,$style,[Drawing.GraphicsUnit]::Pixel)
    $brush=Brush $ink
    $format=[Drawing.StringFormat]::new()
    $format.Alignment='Center'
    $g.DrawString($message,$font,$brush,[single]$center,[single]$y,$format)
    $format.Dispose()
    $brush.Dispose()
    $font.Dispose()
}
$preview=[Drawing.Bitmap]::new(720,340)
$g=[Drawing.Graphics]::FromImage($preview)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#212838'))
$g.InterpolationMode='NearestNeighbor'
$g.PixelOffsetMode='Half'
$g.TextRenderingHint='AntiAliasGridFit'
CenterLabel 360 16 '나무 명판 · 주문 카드 v1' 25 '#ffe5bd' $true
CenterLabel 360 52 '원소별 카드 4종 · 빈 슬롯 · 전투 발동과 충전' 14 '#b4bcd3'
$names=@('화염구','연쇄 번개','얼음 방패','돌풍','빈 슬롯','발동 표시')
$files=@('CardFire','CardLightning','CardIce','CardWind','SlotEmpty','CardFire')
for($i=0;$i -lt $files.Count;$i++){
    $x=27+$i*114
    $dest=[Drawing.Rectangle]::new($x,91,88,128)
    $bitmap=[Drawing.Bitmap]::new((Join-Path $out ($files[$i]+'.png')))
    $g.DrawImage($bitmap,$dest)
    $bitmap.Dispose()
    if($i -eq 5){
        $overlay=[Drawing.Bitmap]::new((Join-Path $out 'SlotFlash.png'))
        $g.DrawImage($overlay,$dest)
        $overlay.Dispose()
        $trackImage=[Drawing.Bitmap]::new((Join-Path $out 'ChargeTrack.png'))
        $g.DrawImage($trackImage,[Drawing.Rectangle]::new($x,225,88,10))
        $trackImage.Dispose()
        $fillImage=[Drawing.Bitmap]::new((Join-Path $out 'ChargeFill.png'))
        $g.DrawImage($fillImage,[Drawing.Rectangle]::new(($x+2),227,52,6))
        $fillImage.Dispose()
    }
    if($i -lt 4 -or $i -eq 5){
        $spellIndex=if($i -eq 5){0}else{$i}
        CenterLabel ($x+44) 164 $names[$spellIndex] 11 '#fff2df' $true
        CenterLabel ($x+44) 188 (@('4','3','2','2')[$spellIndex]) 17 '#3e2c31' $true
    }
    CenterLabel ($x+44) 252 (@('불','번개','얼음','바람','빈 슬롯','발동 표시')[$i]) 15 '#ffe5bd' $true
}
CenterLabel 360 295 '카드 이름과 숫자는 게임에서 렌더링해요.' 14 '#b4bcd3'
$g.Dispose()
$preview.Save((Join-Path $out 'preview.png'),[Drawing.Imaging.ImageFormat]::Png)
$preview.Dispose()

