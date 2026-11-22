$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$asset=Join-Path $PSScriptRoot '../../../the-mage-next-run/Assets/Art/PixelArt/ui/speaker-scroll.png'
$src=[Drawing.Bitmap]::new($asset)
$board=[Drawing.Bitmap]::new(738,285)
$g=[Drawing.Graphics]::FromImage($board)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#171b2a'))
$g.InterpolationMode='NearestNeighbor'
$g.PixelOffsetMode='Half'
$g.TextRenderingHint='AntiAliasGridFit'
Label 23 14 '웨이브 준비 · 안내 양피지' 25 '#ffe9cf' $true
Label 24 65 '게임 문구 예시' 15 '#d7b890' $true
$x=@(24,48,455,479)
$y=@(97,121,150,174)
for($r=0;$r -lt 3;$r++){
    for($c=0;$c -lt 3;$c++){
        $dst=[Drawing.Rectangle]::new($x[$c],$y[$r],($x[$c+1]-$x[$c]),($y[$r+1]-$y[$r]))
        $g.DrawImage($src,$dst,($c*12),($r*12),12,12,[Drawing.GraphicsUnit]::Pixel)
    }
}
$f=[Drawing.Font]::new('Malgun Gothic',23,[Drawing.GraphicsUnit]::Pixel)
$ink=Brush '#4f3333'
$fmt=[Drawing.StringFormat]::new()
$fmt.Alignment='Center'
$fmt.LineAlignment='Center'
$g.DrawString('목표 9 · 적 6마리 (근거리 4 · 원거리 2)',$f,$ink,[Drawing.RectangleF]::new(24,97,455,77),$fmt)
$fmt.Dispose(); $ink.Dispose(); $f.Dispose()
Label 536 65 '원본 스프라이트' 15 '#d7b890' $true
$g.DrawImage($src,[Drawing.Rectangle]::new(539,91,144,144))
Label 24 208 '준비 화면 상단에서 목표 합계와 적 구성을 보여주는 배너' 14 '#c4c2d3'
$g.Dispose()
$board.Save((Join-Path $PSScriptRoot 'forecast-parchment.png'),[Drawing.Imaging.ImageFormat]::Png)
$src.Dispose(); $board.Dispose()
