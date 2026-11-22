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
function Star($x,$y,$c) {
    Pixel ($x-2) $y 5 1 $c
    Pixel $x ($y-2) 1 5 $c
}
function Wizard($design) {
    $ink='#31243d'; $shadow='#46365d'; $main='#65549a'; $light='#8a78c4'; $trim='#ffd781'
    if ($design -eq 2) { $ink='#21334d'; $shadow='#344d70'; $main='#4e729b'; $light='#81a6c8'; $trim='#a9f1e1' }
    if ($design -eq 3) { $ink='#492b42'; $shadow='#85495e'; $main='#be6474'; $light='#e98b91'; $trim='#ffdf9f' }
    # Tail of the cape, boots and tunic.
    Shape $ink @(9,15,19,15,21,24,19,26,20,28,15,28,14,26,13,28,8,28,8,26,3,25,6,22)
    Shape $shadow @(10,16,18,17,19,24,16,25,10,25,5,24,8,22)
    Shape $main @(11,17,17,17,17,22,16,24,9,24,11,21)
    Pixel 9 26 3 1 '#9e7375'
    Pixel 16 26 3 1 '#9e7375'
    # Hair and visible face.
    Shape $ink @(9,10,19,9,21,11,21,16,19,19,13,19,10,17,8,16)
    Shape '#cf8a78' @(12,12,20,11,20,16,18,18,14,18,12,16)
    Shape '#ffd5a3' @(13,12,20,12,20,15,18,17,15,17,13,15)
    Pixel 12 13 2 2 '#774b58'
    Pixel 16 13 1 2 $ink
    Pixel 19 13 1 2 $ink
    Pixel 15 15 2 1 '#f59488'
    Pixel 18 16 1 1 '#a86068'
    # Swept star hat, moon hood, or layered petal cap.
    switch ($design) {
        1 {
            Shape $ink @(4,11,7,9,8,6,11,3,15,2,20,2,20,4,16,5,16,7,20,9,24,9,24,11,21,13,12,13,6,14,4,13)
            Shape $main @(6,11,9,9,10,6,13,4,17,3,18,3,15,5,15,8,18,10,22,10,20,11,11,12,6,13)
            Shape $light @(9,9,10,6,13,4,16,4,13,6,12,9)
            Shape $trim @(8,10,17,8,19,9,13,11,8,12)
            Pixel 13 8 2 2 '#fff1ba'
        }
        2 {
            Shape $ink @(6,9,7,6,10,3,14,2,18,3,21,6,23,10,22,12,18,12,16,10,12,12,12,17,10,19,6,17,5,14)
            Shape $main @(7,9,8,6,11,4,15,3,19,5,21,8,22,11,18,10,16,9,12,10,10,13,10,17,7,16,6,13)
            Shape $light @(7,10,8,7,11,5,15,4,17,5,12,6,9,9,8,14,7,15)
            Pixel 15 6 2 2 $trim
            Pixel 17 7 2 1 $trim
            Pixel 16 8 2 1 $trim
        }
        3 {
            Shape $ink @(4,8,8,7,9,4,12,2,15,3,17,2,20,4,20,6,24,7,24,10,20,13,10,13,5,11)
            Shape $main @(5,9,9,8,10,5,12,3,15,5,17,3,19,5,18,8,23,8,23,10,19,12,11,12,6,10)
            Shape $light @(6,9,10,9,11,5,12,4,14,7,17,5,17,8,14,10,10,11)
            Pixel 15 9 3 2 $trim
            Pixel 16 9 1 1 '#fff2c7'
        }
    }
    # Cape clasp and staff silhouette.
    Pixel 13 19 3 2 $trim
    Pixel 14 19 1 1 '#fff4d3'
    Pixel 23 11 2 17 $ink
    Pixel 24 12 1 14 '#a46359'
    Pixel 21 19 3 3 $ink
    Pixel 21 19 2 2 '#f3b38e'
    switch ($design) {
        1 {
            Shape $ink @(24,4,26,4,27,7,30,8,30,10,27,11,26,14,24,14,23,11,20,10,20,8,23,7)
            Star 25 9 $trim
            Pixel 25 8 1 2 '#fff4c5'
        }
        2 {
            Shape $ink @(24,4,28,4,28,6,26,7,26,9,28,10,30,8,31,9,30,12,28,14,24,14,21,11,21,7)
            Shape $trim @(24,5,27,5,25,7,25,10,27,12,29,11,28,13,24,13,22,11,22,8)
            Pixel 23 8 1 2 '#e5ffec'
        }
        3 {
            Shape $ink @(23,5,26,5,27,7,29,7,30,9,29,11,27,11,26,14,23,14,22,12,20,11,20,8,22,7)
            Star 25 9 '#ffa8b4'
            Pixel 24 8 2 2 $trim
            Pixel 25 7 1 1 '#ffe0d1'
        }
    }
}
function Slime($design) {
    $ink='#234c57'; $shadow='#367d84'; $main='#60b8b2'; $light='#9be4d3'; $shine='#e1fff1'; $cheek='#f5adb2'
    switch ($design) {
        1 {
            Shape $ink @(17,10,19,10,20,13,23,15,26,19,27,23,26,26,23,28,9,28,5,26,4,23,5,20,9,16,14,14)
            Shape $shadow @(17,12,18,12,19,14,22,16,25,20,26,23,25,25,22,27,9,27,6,25,5,23,7,20,10,17,15,15)
            Shape $main @(17,13,19,15,22,17,25,21,25,23,22,25,9,25,6,23,9,19,13,17,16,16)
            Shape $light @(15,16,18,14,21,17,23,20,20,21,10,20,11,18)
            Pixel 14 17 3 1 $shine
            Pixel 13 18 1 1 $shine
        }
        2 {
            $ink='#673548'; $shadow='#b96071'; $main='#ef8b8c'; $light='#ffb2a5'; $shine='#ffe0bd'; $cheek='#c95273'
            Shape $ink @(8,15,13,13,16,14,20,13,24,14,27,17,28,21,27,25,24,27,20,28,10,28,6,27,3,24,3,20,5,17)
            Shape $shadow @(8,16,13,14,16,15,20,14,24,15,26,18,27,21,26,24,23,26,20,27,10,27,6,26,4,23,4,20)
            Shape $main @(7,17,13,15,16,16,20,15,24,16,26,20,25,23,21,25,10,25,5,23,5,20)
            Shape $light @(7,18,12,16,15,16,16,18,20,16,23,16,25,19,22,21,8,21,6,20)
            Pixel 10 17 3 1 $shine
            Pixel 9 18 1 1 $shine
            Shape '#53664a' @(15,15,16,11,19,10,23,10,21,13,18,14,17,16)
            Pixel 18 11 3 1 '#a4cd76'
        }
        3 {
            $ink='#414e38'; $shadow='#718349'; $main='#a6b45f'; $light='#d7df88'; $shine='#f7f2b5'; $cheek='#ec9f89'
            Shape $ink @(9,16,14,15,16,15,19,14,24,16,27,19,28,23,26,26,23,28,8,28,4,26,3,23,4,20)
            Shape $shadow @(9,17,14,16,16,16,19,15,24,17,26,20,27,23,25,25,22,27,8,27,5,25,4,23,6,20)
            Shape $main @(10,18,19,16,24,18,26,21,25,24,21,25,9,25,5,23,7,20)
            Shape $light @(8,20,11,18,19,17,23,18,24,20,20,21,8,22)
            Pixel 9 19 3 1 $shine
            Shape '#374f3b' @(16,18,16,14,11,14,8,11,8,8,12,9,16,11,17,9,20,7,24,7,24,10,21,13,18,14,18,17)
            Shape '#77ab62' @(9,9,12,10,15,12,12,13,10,11)
            Shape '#a1cb74' @(17,12,19,9,23,8,22,10,20,12)
        }
    }
    Pixel 8 21 1 2 $ink
    Pixel 15 21 1 2 $ink
    Pixel 6 23 2 1 $cheek
    Pixel 16 23 2 1 $cheek
    if ($design -eq 2) {
        Pixel 11 22 2 2 $ink
        Pixel 11 23 2 1 '#ffa7a1'
    } else {
        Pixel 11 23 2 1 $ink
        Pixel 12 24 1 1 $ink
    }
}
function OpenBitmap($path) { [Drawing.Bitmap]::new((Join-Path $root $path)) }
$terrain = OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$oldWizard = OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$oldSlime = OpenBitmap 'exports/v1/meadow-slime/idle/slime32_idle.png'
$board = [Drawing.Bitmap]::new(756,480)
$entries = @(
    @{ Label='기존'; Wizard='후드 마법사'; Slime='초원 슬라임' },
    @{ Label='A'; Wizard='별우편 마법사'; Slime='이슬방울 슬라임' },
    @{ Label='B'; Wizard='달빛 마법사'; Slime='복숭아 슬라임' },
    @{ Label='C'; Wizard='꽃잎 마법사'; Slime='새싹 슬라임' }
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
    if ($design -eq 0) {
        $g.DrawImage($old,[Drawing.Rectangle]::new(0,0,32,32),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
    } else {
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
