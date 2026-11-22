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
        J='#685143'; V='#ad8154'; Y='#e4bd7c'
        S='#b97562'; F='#ebad83'; H='#fbe0b4'; E='#422a38'; I='#edf2e4'; U='#435779'
        T='#674436'; W='#aa704e'; G='#d9a366'; A='#68c8b7'; C='#d6fff0'; M='#36818a'
    }
    $rows=@(
        '.........KKK............'
        '........KWYKK...........'
        '.......KYHYVYKK.........'
        '......KYHYVYVJKK........'
        '.......KFJYFYVJKK.......'
        '.......KFIEFSJVYKK......'
        '.......KFFFSKJVYK.......'
        '........KSSKK.KVK.......'
        '......KKKHHHKKWKK...KK..'
        '.....KDBNHHDNGNBDK.KCAK.'
        '....KNBBNDNBBGNBBDKKCMK.'
        '..KKDNBNNDBBBNDNBBKKWK..'
        '.KFSKNNBNDLLBNDNBBKKWK..'
        'KFSFKNBDNNBBNDNBKKKTK...'
        '.KSSKKKDNNDNDDKFSSKWK...'
        '..KK..KNDDGGGKKFSSKTK...'
        '.....KNDNDGWTNNDKKKWK...'
        '.....KNDNDWTDNBNDK.TK...'
        '.....KNDNWTKDBNBDK.WK...'
        '....KBNDDWTK.DBNNK.TK...'
        '....KNDDKTK..KDBNK.WK...'
        '....KDDKDNK..KDNK..TK...'
        '....KDDKDBK..KDNK..TK...'
        '....KKKKTWK..KTWK..WK...'
        '......KTWWK..KTWWK.KK...'
        '......KKKKK..KKKKK......'
    )
    # Keep the silhouettes and material clusters on the logical pixel grid.
    for ($y=0; $y -lt $rows.Count; $y++) {
        for ($x=0; $x -lt $rows[$y].Length; $x++) {
            $key=[string]$rows[$y][$x]
            if ($key -ne '.' -and $x -lt 18) { Pixel ($x+4) ($y+2) 1 1 $palette[$key] }
        }
    }
    # The shaft remains on one column from the crystal socket to the tip.
    Pixel 24 9 3 19 '#251f31'
    Pixel 25 10 1 17 '#aa704e'
    Pixel 25 10 1 2 '#d9a366'
    Pixel 25 20 1 2 '#d9a366'
    Pixel 23 7 5 3 '#251f31'
    Pixel 24 6 3 5 '#251f31'
    Pixel 25 5 1 1 '#251f31'
    Pixel 24 7 3 2 '#68c8b7'
    Pixel 25 6 1 3 '#d6fff0'
    Pixel 25 9 1 1 '#36818a'
    Pixel 22 16 3 2 '#251f31'
    Pixel 22 16 1 1 '#76577d'
    Pixel 23 16 3 2 '#b97562'
    Pixel 24 16 1 1 '#ebad83'
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
        $sprite.RotateFlip([Drawing.RotateFlipType]::RotateNoneFlipX)
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
$labels=@('기존','전투 도트 비율 수정')
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














