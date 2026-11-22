$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$out = $PSScriptRoot
$root = Join-Path $out '../..'
function Pixel($x,$y,$w,$h,$color) {
    $brush = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml($color))
    $g.FillRectangle($brush,[int]$x,[int]$y,[int]$w,[int]$h)
    $brush.Dispose()
}
function Traveler {
    $palette=@{
        K='#251f31'; D='#372b46'; N='#544167'; B='#76577d'; L='#ac7a91'
        R='#4c2c30'; J='#774044'; V='#a45346'; Y='#d87d56'
        S='#b97562'; F='#ebad83'; H='#fbe0b4'; E='#422a38'; I='#edf2e4'; U='#435779'
        T='#674436'; W='#aa704e'; G='#d9a366'; A='#68c8b7'; C='#d6fff0'; M='#36818a'
    }
    $rows=@(
        '.........KKKKK..........'
        '.......KKJVVVJKK........'
        '......KRVVYYVVVJK.......'
        '.....KJVYVVJVVVVRK...K..'
        '.....KRVVJVVJYVVRK..KCK.'
        '.....KRVJVSFFFVJJK..KCAK'
        '.....KRJVSFFFFSJRK.KCMAK'
        '......KJSIEFFIERSK.KAMK.'
        '......KJSFEFFEFK...KWK..'
        '.......KSSFFFFSK...KWK..'
        '........KKSSSKK....KWK..'
        '......KKNDKHKNNKK..KTK..'
        '.....KNBNGHHDNBNK..KWK..'
        '....KNBLBGHFDNBNKK.KTK..'
        '....KBNBNGHDNBBNFSKKWK..'
        '....KBNDNGDDKNBNFFSKTK..'
        '....KNNDKGGGKDDKKSSKWK..'
        '....KNDDKWTWGGDK..KTK...'
        '....KNDDKWWTGDNK..KWK...'
        '....KNDDKWTKBNNK..KTK...'
        '...KNDDDKWTKNDNK..KWK...'
        '...KNDDKKTKKKNDNK.KTK...'
        '...KNDKKTK..KNDK..KWK...'
        '...KKKKKWK..KTWK..KTK...'
        '......KWWK..KTWWK.KWK...'
        '......KKKK..KKKKK.KKK...'
    )
    # Keep the silhouettes and material clusters on the logical pixel grid.
    for ($y=0; $y -lt $rows.Count; $y++) {
        for ($x=0; $x -lt $rows[$y].Length; $x++) {
            $key=[string]$rows[$y][$x]
            if ($key -ne '.') { Pixel ($x+4) ($y+2) 1 1 $palette[$key] }
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
$labels=@('기존','표지 마법사 · 전투 자세')
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









