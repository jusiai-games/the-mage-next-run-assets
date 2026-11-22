$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$sprites=Join-Path $PSScriptRoot '../../exports/v1/spells-to-go-ui/package/Assets/SpellsToGo/UI/Sprites'
$board=[Drawing.Bitmap]::new(790,418)
$g=[Drawing.Graphics]::FromImage($board)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#171b2a'))
$g.InterpolationMode='NearestNeighbor'
$g.PixelOffsetMode='Half'
$g.TextRenderingHint='AntiAliasGridFit'
function ButtonSample($file,$x,$y,$width,$title,$ink){
    $src=[Drawing.Bitmap]::new((Join-Path $sprites "button-$file.png"))
    $edges=@(0,24,($width-24),$width)
    $height=@(0,24,42,66)
    for($r=0;$r -lt 3;$r++){
        for($c=0;$c -lt 3;$c++){
            $dst=[Drawing.Rectangle]::new(($x+$edges[$c]),($y+$height[$r]),($edges[$c+1]-$edges[$c]),($height[$r+1]-$height[$r]))
            $g.DrawImage($src,$dst,($c*12),($r*12),12,12,[Drawing.GraphicsUnit]::Pixel)
        }
    }
    $src.Dispose()
    $font=[Drawing.Font]::new('Malgun Gothic',18,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
    $brush=Brush $ink
    $format=[Drawing.StringFormat]::new()
    $format.Alignment='Center'
    $format.LineAlignment='Center'
    $g.DrawString($title,$font,$brush,[Drawing.RectangleF]::new($x,($y+1+$([int]($file -eq 'pressed')*2)),$width,66),$format)
    $font.Dispose()
    $brush.Dispose()
    $format.Dispose()
}
Label 25 18 '주문 넣고 갑니다 · v1 버튼' 26 '#ffe9cf' $true
Label 27 71 '버튼 상태' 17 '#d7b890' $true
$states=@('normal','highlighted','pressed','disabled')
$stateTitles=@('기본','강조·선택','눌림','비활성')
for($i=0;$i -lt 4;$i++){
    ButtonSample $states[$i] (27+186*$i) 103 175 $stateTitles[$i] $(switch($i){2{'#fff0d9'} 3{'#54463f'} default{'#2b2028'}})
}
Rect 27 197 736 1 '#514053'
Label 27 211 '게임에서 쓰는 문구' 17 '#d7b890' $true
Label 27 255 '진행' 14 '#c3c6d4'
ButtonSample 'normal' 119 238 173 '게임 시작' '#2b2028'
ButtonSample 'normal' 305 238 173 '전투 시작' '#2b2028'
ButtonSample 'normal' 491 238 173 '출발' '#2b2028'
Label 27 332 '희생·확인' 14 '#c3c6d4'
ButtonSample 'normal' 119 315 173 '희생' '#2b2028'
ButtonSample 'normal' 305 315 173 '취소' '#2b2028'
ButtonSample 'normal' 491 315 173 '확인' '#2b2028'
$g.Dispose()
$board.Save((Join-Path $PSScriptRoot 'buttons.png'),[Drawing.Imaging.ImageFormat]::Png)
$board.Dispose()


