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
function Traveler($variant) {
    $ink='#1d2232'; $deep='#2b344c'; $robe='#415474'; $rim='#647e98'
    $skin='#ce977b'; $shine='#efd0a5'; $hair='#594342'
    $wood='#785343'; $edge='#b58762'
    # The coat opens over trousers, leaving a clear gap between the boots.
    Shape $ink @(11,12,20,11,23,15,22,19,20,21,22,27,20,28,15,28,14,25,11,28,6,28,6,26,8,22,3,24,3,21,6,17)
    Shape $deep @(11,13,19,12,21,15,20,20,18,21,20,26,16,26,14,23,10,26,8,26,10,22,5,23,6,20)
    Shape $robe @(9,15,13,13,15,16,12,20,9,22,5,22,7,18)
    Shape $rim @(8,17,11,15,12,16,9,20,6,21)
    Pixel 7 26 4 1 '#8b7262'
    Pixel 16 26 4 1 '#8b7262'
    Pixel 13 19 6 2 $wood
    Pixel 17 19 2 1 '#cfab71'
    # Low hood opening, forward glance and a lock of swept hair.
    Shape $ink @(8,11,8,7,11,4,15,2,19,3,22,5,24,9,22,12,19,14,15,14,12,12,9,14)
    Shape $robe @(9,10,9,7,12,5,15,3,19,4,21,5,23,8,20,7,16,8,13,11,10,13)
    Shape $rim @(10,8,12,5,15,4,18,4,15,6,12,7,11,10)
    Shape $skin @(15,9,19,7,21,8,22,10,20,11,19,13,16,12)
    Pixel 19 9 2 1 $ink
    Pixel 20 10 1 1 $shine
    Pixel 18 12 1 1 '#7d5050'
    Shape $hair @(14,10,16,8,19,7,21,8,18,8,17,10,15,11)
    # Each pose uses a plain wood staff with a different grip.
    if ($variant -eq 2) {
        Shape $ink @(5,8,6,6,10,7,12,9,17,10,22,13,29,16,30,18,28,19,22,16,17,13,12,12,7,10)
        Shape $wood @(6,8,7,7,10,8,12,10,17,11,22,14,29,17,28,18,22,15,17,12,12,11,7,9)
        Pixel 17 11 3 1 $edge
        Pixel 22 13 2 2 $skin
        Pixel 23 13 1 1 $shine
        Shape '#948b72' @(12,16,15,16,16,18,15,19,12,19)
    } else {
        Shape $ink @(24,26,25,15,25,11,23,8,23,5,25,3,29,3,31,5,31,8,29,9,28,12,28,18,27,27)
        Shape $wood @(25,26,26,15,26,11,24,8,24,5,26,4,29,4,30,5,30,8,28,8,27,12,27,18,26,26)
        Shape $edge @(24,6,26,4,29,4,29,5,26,5,25,7)
        Pixel 26 12 2 1 '#c3b091'
        Pixel 26 14 2 1 '#a2947a'
        Shape $ink @(17,14,20,12,22,15,26,15,27,18,23,20,19,19)
        Shape $rim @(18,14,20,13,21,15,20,17,18,17)
        Pixel 22 16 3 2 $skin
        Pixel 24 16 1 1 $shine
    }
    switch ($variant) {
        1 {
            Shape $ink @(8,17,12,18,14,22,12,25,7,24,6,21)
            Shape '#726447' @(8,18,11,19,13,22,12,24,8,23,7,21)
            Shape '#cbc39d' @(8,16,10,16,11,22,9,22)
            Pixel 10 17 2 1 '#dfd2ae'
            Pixel 9 21 3 1 '#575b53'
        }
        2 {
            Pixel 17 12 2 1 '#f7cda0'
            Pixel 19 12 1 1 '#664351'
            Shape '#8b6b4a' @(8,16,10,14,10,16,9,18,6,19,5,18)
            Pixel 7 17 2 1 '#b89665'
        }
        3 {
            Shape $ink @(3,19,7,18,9,16,12,16,11,19,8,22,2,22)
            Shape '#536b60' @(3,20,7,19,9,17,11,17,10,19,7,21,3,21)
            Pixel 11 15 2 1 '#c9ac70'
            Pixel 27 6 2 1 '#a1e2d6'
            Pixel 28 5 1 3 '#dcfff0'
        }
    }
}

function OpenBitmap($path) { [Drawing.Bitmap]::new((Join-Path $root $path)) }
function Label($value,$x,$y,$size,$color) {
    $font=[Drawing.Font]::new('Malgun Gothic',$size,[Drawing.GraphicsUnit]::Pixel)
    $brush=[Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.DrawString($value,$font,$brush,[single]$x,[single]$y)
    $font.Dispose()
    $brush.Dispose()
}
function Frame($index) {
    $sprite=[Drawing.Bitmap]::new(32,32)
    $g=[Drawing.Graphics]::FromImage($sprite)
    if ($index -eq 0) {
        $g.DrawImage($original,[Drawing.Rectangle]::new(0,0,32,32),0,0,32,32,[Drawing.GraphicsUnit]::Pixel)
    } else {
        Traveler $index
        foreach ($y in 0..31) {
            foreach ($x in 0..31) {
                $alpha=$sprite.GetPixel($x,$y).A
                if ($alpha -notin @(0,255) -or ($alpha -gt 0 -and $y -ge 28)) {
                    throw "Invalid pixel at $x,$y"
                }
            }
        }
        $sprite.Save((Join-Path $out "$($ids[$index])-wizard.png"),[Drawing.Imaging.ImageFormat]::Png)
    }
    $g.Dispose()
    $sprite
}
$ids=@('original','a','b','c')
$labels=@('기존','A · 주문 수집가','B · 허세 섞인 여유','C · 한 박자 먼저')
$original=OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$terrain=OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$board=[Drawing.Bitmap]::new(756,332)
$g=[Drawing.Graphics]::FromImage($board)
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
$g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::AntiAliasGridFit
Pixel 0 0 756 332 '#242735'
Label '초원을 지키는 후드 마법사' 20 14 24 '#fff0d5'
Label '주인공 시안  ·  최근접 4배 확대와 초원 1배 비교' 20 49 14 '#d2c3cb'
for ($i=0; $i -lt 4; $i++) {
    $x=18+182*$i
    $sprite=Frame $i
    Pixel $x 80 174 234 '#343b50'
    Label $labels[$i] ($x+10) 88 15 '#ffe0ac'
    Pixel ($x+8) 116 158 136 '#505a70'
    $g.DrawImage($sprite,[Drawing.Rectangle]::new(($x+23),119,128,128))
    $g.DrawImage($terrain,[Drawing.Rectangle]::new(($x+7),264,160,42),0,50,160,42,[Drawing.GraphicsUnit]::Pixel)
    $g.DrawImage($sprite,($x+15),265,32,32)
    $sprite.Dispose()
}
$board.Save((Join-Path $out 'comparison.png'),[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$board.Dispose()
$terrain.Dispose()
$original.Dispose()
