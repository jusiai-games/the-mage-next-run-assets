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
function Traveler {
    $ink='#25212b'; $shade='#33374b'; $coat='#4a5269'; $seam='#697b91'
    $sand='#bb9a71'; $darkSand='#866953'
    $hair='#4c393c'; $hairLight='#795750'
    $skin='#c88769'; $lit='#efbd94'
    # Long coat with an open front and a low sweep to the left.
    Shape $ink @(10,10,18,9,21,11,22,15,20,18,22,22,24,25,21,26,21,28,16,28,16,25,14,22,12,25,12,28,7,28,7,26,3,27,2,25,5,22,6,16)
    Shape $shade @(10,11,17,10,20,12,20,16,18,18,20,22,22,24,19,25,19,27,17,27,17,24,14,20,12,23,10,26,8,26,9,24,5,26,4,25,7,22,7,17)
    Shape $coat @(9,12,12,12,13,15,12,18,10,21,8,24,5,25,7,22,8,16)
    Shape $seam @(8,15,10,13,11,14,9,18,8,21,7,22)
    Shape '#2b2934' @(15,16,18,16,19,21,21,24,18,24,16,21,14,20)
    Pixel 9 26 3 1 '#94745e'
    Pixel 17 26 3 1 '#94745e'
    # Stand collar and the inner fold, cut as two distinct planes.
    Shape $darkSand @(9,9,13,10,15,13,14,16,11,14)
    Shape $sand @(10,10,12,11,14,13,14,14,12,13)
    Pixel 15 12 2 1 '#d5b28a'
    Pixel 13 18 5 1 '#916c53'
    Pixel 16 18 2 1 '#ddba85'
    # Brushed-back silhouette and one loose lock.
    Shape $ink @(10,8,10,5,9,3,12,3,15,1,19,1,22,2,24,4,23,6,22,7,23,8,22,10,20,11,19,13,15,13,12,11)
    Shape $hair @(11,7,11,5,10,4,13,4,15,2,19,2,22,3,23,4,21,6,17,6,15,8,14,10,12,9)
    Shape $hairLight @(12,5,15,3,19,3,20,4,17,4,15,5,13,7)
    Shape $skin @(16,7,19,5,22,6,22,8,23,8,22,9,21,10,20,11,17,11,15,9)
    Shape $lit @(18,7,20,6,22,7,21,9,20,10,18,10,17,9)
    Pixel 19 7 3 1 $ink
    Pixel 20 9 1 1 '#89534f'
    Pixel 16 8 1 1 '#966051'
    # Flat hip satchel and a rolled spell page lit at its folded edge.
    Shape $ink @(8,17,12,18,13,22,11,25,7,24,6,22)
    Shape '#775d50' @(8,18,11,19,12,22,11,24,8,23,7,22)
    Pixel 8 20 3 1 $sand
    Shape $ink @(7,16,10,15,12,16,11,19,8,20,7,19)
    Shape '#e1c397' @(8,16,10,16,11,17,10,19,8,19)
    Pixel 9 16 1 1 '#f6dec0'
    # The existing mage role reads through a spare wooden staff.
    Shape $ink @(26,28,25,26,26,16,26,9,25,6,26,4,28,2,31,2,32,4,30,5,28,5,28,8,29,10,28,19,28,27)
    Shape '#896550' @(26,26,27,16,27,9,26,6,27,4,29,3,31,3,30,4,28,4,27,6,28,9,27,19,27,26)
    Pixel 28 3 2 1 '#d7ab7f'
    Pixel 27 10 1 2 '#c9af8e'
    Shape $ink @(18,12,20,11,22,13,23,15,26,14,29,14,29,17,25,18,21,17,19,15)
    Shape $coat @(19,12,20,12,22,14,23,16,25,15,25,16,24,17,22,16,20,15)
    Pixel 24 15 1 2 $sand
    Pixel 26 15 2 2 $skin
    Pixel 27 15 1 1 $lit
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
        Traveler
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
$ids=@('original','hero')
$labels=@('기존','두루마리 마법사')
$original=OpenBitmap 'exports/v1/wizard/idle/hood_staff_idle.png'
$terrain=OpenBitmap 'exports/v1/meadow-wave-mobile/meadow-terrain.png'
$board=[Drawing.Bitmap]::new(392,332)
$g=[Drawing.Graphics]::FromImage($board)
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::Half
$g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::AntiAliasGridFit
Pixel 0 0 392 332 '#242735'
Label '마법사 주인공 비교' 20 14 24 '#fff0d5'
Label '4배 확대  ·  초원 위 1배' 20 49 14 '#d2c3cb'
for ($i=0; $i -lt 2; $i++) {
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



