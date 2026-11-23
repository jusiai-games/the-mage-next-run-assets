$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'render-variants.ps1') -DefinitionsOnly

$out=Join-Path $PSScriptRoot '../../exports/v1/wood-spell-cards'
New-Item -ItemType Directory -Path $out -Force | Out-Null
$elements=@(
    @{file='CardFire'; icon=0; deep='#703833'; mid='#ee7547'; light='#ffda83'},
    @{file='CardLightning'; icon=1; deep='#274969'; mid='#73b8e2'; light='#e2f9ff'},
    @{file='CardIce'; icon=3; deep='#305c5e'; mid='#78cbbd'; light='#d5fff2'}
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
