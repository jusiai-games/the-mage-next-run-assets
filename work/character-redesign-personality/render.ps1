$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$out = $PSScriptRoot
$root = Join-Path $out '../..'
function Pixel($x,$y,$w,$h,$color) {
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.FillRectangle($brush,[int]$x,[int]$y,[int]$w,[int]$h)
    $brush.Dispose()
}
function Shape($color,[int[]]$coords) {
    [Drawing.Point[]]$points = for ($i=0; $i -lt $coords.Count; $i+=2) {
        [Drawing.Point]::new($coords[$i],$coords[$i+1])
    }
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.FillPolygon($brush,$points)
    $brush.Dispose()
}
function Wizard($design) {
    $ink='#1d2035'; $shade='#292d49'; $cloth='#3c456b'; $light='#626b97'
    $skin='#d39876'; $skinLight='#f1ba91'
    # Rebuild the opening of the hood so that the eye and brow read separately.
    Shape $ink @(15,10,19,8,21,8,22,10,21,12,19,14,16,14)
    Shape $skin @(17,10,20,9,21,10,21,11,19,13,17,13)
    Pixel 19 11 2 1 $skinLight
    switch ($design) {
        1 {
            # Raised brow, asymmetric grin, and a scarf trailing behind.
            Pixel 18 9 2 1 '#767eaa'
            Pixel 19 10 1 1 $ink
            Pixel 18 12 2 1 '#392839'
            Pixel 19 12 1 1 '#ffe4bd'
            Shape $ink @(14,13,14,16,10,17,9,19,4,20,3,18,6,16,10,16)
            Shape '#7d5359' @(13,14,13,16,9,16,8,18,4,19,5,17,9,17)
            Shape '#b77971' @(6,17,10,17,12,15,13,15,10,18,6,18)
        }
        2 {
            # Head tucked low, scuffed hem, and a hastily patched shoulder.
            Shape $cloth @(13,10,19,8,22,8,21,10,17,11,14,12)
            Pixel 18 10 2 1 $ink
            Pixel 20 11 1 1 $skinLight
            Pixel 17 12 2 1 '#694553'
            Shape $ink @(11,15,14,14,17,16,15,19,12,19,10,17)
            Shape '#747b91' @(11,16,14,15,16,16,14,18,12,18)
            Pixel 12 16 2 1 '#abb0bd'
            Pixel 9 24 2 1 '#777b9a'
            Pixel 10 23 1 1 '#aaa0a1'
            Pixel 25 14 1 3 '#d7b894'
            Pixel 24 16 2 1 '#b79c85'
        }
        3 {
            # Open hood edge, visible lock of hair, and a hand-worn cape clasp.
            Pixel 17 9 2 2 '#644448'
            Pixel 17 9 1 1 '#a97057'
            Pixel 19 10 1 1 $ink
            Pixel 18 12 2 1 '#885857'
            Shape $ink @(12,14,15,13,17,15,16,17,13,18,11,16)
            Shape '#b59165' @(12,15,15,14,16,15,15,17,13,17)
            Pixel 14 15 1 1 '#f3d39c'
            Shape $shade @(12,18,15,19,13,21,10,23,10,21)
            Shape $light @(11,20,13,19,12,21,10,22)
        }
    }
}
function Slime($design) {
    $ink='#193b36'; $body='#5eac8f'; $light='#b8edc7'
    Shape $body @(5,15,18,15,20,22,16,24,6,23,4,20,5,19)
    switch ($design) {
        1 {
            Shape $ink @(6,16,10,17,10,20,7,19)
            Shape $ink @(12,17,16,15,17,17,15,20,12,19)
            Pixel 9 21 4 1 $ink
            Pixel 12 20 1 1 $ink
            Pixel 8 18 1 1 $light
            Pixel 14 17 1 1 $light
        }
        2 {
            Shape $ink @(5,16,10,18,10,20,6,19)
            Shape $ink @(12,18,17,16,17,19,13,20)
            Pixel 8 22 5 1 $ink
            Pixel 7 23 1 1 $ink
            Pixel 13 23 1 1 $ink
            Pixel 6 14 2 1 '#368471'
            Pixel 5 15 2 1 '#368471'
        }
        3 {
            Pixel 6 16 3 3 $ink
            Pixel 12 17 3 2 $ink
            Pixel 6 16 1 1 $light
            Pixel 12 17 1 1 $light
            Pixel 9 21 2 1 $ink
            Pixel 10 22 1 1 $ink
            Pixel 11 15 2 1 '#368471'
        }
    }
}
function OpenBitmap($path) { [Drawing.Bitmap]::new((Join-Path $root $path)) }
$terrain = OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$oldWizard = OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$oldSlime = OpenBitmap 'exports/v1/meadow-slime/idle/slime32_idle.png'
$board = [Drawing.Bitmap]::new(756,480)
$entries = @(
    @{ Label='기존'; Wizard='후드 마법사'; Slime='초원 슬라임' },
    @{ Label='A'; Wizard='허세 부리는 신참'; Slime='심술쟁이' },
    @{ Label='B'; Wizard='끝까지 버티는 녀석'; Slime='오기 많은 녀석' },
    @{ Label='C'; Wizard='말보다 행동'; Slime='눈치 빠른 녀석' }
)
function Text($value,$x,$y,$size,$color) {
    $font = [Drawing.Font]::new('Malgun Gothic',$size,[Drawing.GraphicsUnit]::Pixel)
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.DrawString($value,$font,$brush,[single]$x,[single]$y)
    $font.Dispose()
    $brush.Dispose()
}
function Sprite($kind,$design,$old) {
    $sprite = [Drawing.Bitmap]::new(32,32)
    $g = [Drawing.Graphics]::FromImage($sprite)
    $g.DrawImage($old,[Drawing.Rectangle]::new(0,0,32,32),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
    if ($design -ne 0) {
        if ($kind -eq 'wizard') { Wizard $design } else { Slime $design }
        $prefix = $entries[$design].Label.ToLowerInvariant()
        $sprite.Save((Join-Path $out "$prefix-$kind.png"),[Drawing.Imaging.ImageFormat]::Png)
        for ($x=0; $x -lt 32; $x++) {
            for ($y=0; $y -lt 32; $y++) {
                $alpha = $sprite.GetPixel($x,$y).A
                if ($alpha -notin @(0,255) -or ($alpha -gt 0 -and $y -ge 28)) { throw "Invalid sprite pixel at $x,$y" }
            }
        }
    }
    $g.Dispose()
    $sprite
}
$g = [Drawing.Graphics]::FromImage($board)
$g.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode = [Drawing.Drawing2D.PixelOffsetMode]::Half
$g.TextRenderingHint = [Drawing.Text.TextRenderingHint]::AntiAliasGridFit
Pixel 0 0 756 480 '#242332'
Text '마법사와 초원 슬라임' 20 14 24 '#fff0d5'
Text '대기 포즈  ·  최근접 4배 확대와 초원 1배 비교' 21 48 14 '#c6b6c7'
for ($i=0; $i -lt 4; $i++) {
    $x = 18+182*$i
    $wizard = Sprite 'wizard' $i $oldWizard
    $slime = Sprite 'slime' $i $oldSlime
    $entry = $entries[$i]
    Pixel $x 80 174 382 '#333143'
    Text $entry.Label ($x+12) 87 17 '#ffdc9e'
    Pixel ($x+8) 112 158 132 '#454257'
    $g.DrawImage($wizard,[Drawing.Rectangle]::new(($x+23),114,128,128))
    Text $entry.Wizard ($x+10) 248 14 '#fff0d5'
    Pixel ($x+8) 273 158 110 '#454257'
    $g.DrawImage($slime,[Drawing.Rectangle]::new(($x+23),269,128,128))
    Text $entry.Slime ($x+10) 388 14 '#fff0d5'
    $g.DrawImage($terrain,[Drawing.Rectangle]::new(($x+7),410,160,42),0,50,160,42,[Drawing.GraphicsUnit]::Pixel)
    $g.DrawImage($wizard,($x+15),411,32,32)
    $g.DrawImage($slime,($x+105),411,32,32)
    $wizard.Dispose()
    $slime.Dispose()
}
$board.Save((Join-Path $out 'comparison.png'),[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$board.Dispose()
$terrain.Dispose()
$oldWizard.Dispose()
$oldSlime.Dispose()


