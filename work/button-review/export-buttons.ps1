$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../spell-card-concepts/render-variants.ps1') -DefinitionsOnly
$sprites=Join-Path $PSScriptRoot '../../exports/v1/spells-to-go-ui/package/Assets/SpellsToGo/UI/Sprites'
$buttons=@(
    @{id='normal'; outer='#261e2a'; rim='#bf8b65'; bevel='#674534'; face='#9c6e54'; top='#e8b58c'; bottom='#82583f'},
    @{id='highlighted'; outer='#2d2330'; rim='#e9ba72'; bevel='#815238'; face='#ad7b57'; top='#ffe0a4'; bottom='#936447'},
    @{id='pressed'; outer='#291e28'; rim='#a47559'; bevel='#53362d'; face='#714a3a'; top='#75513e'; bottom='#a7795a'},
    @{id='disabled'; outer='#5c4d4c'; rim='#9e8878'; bevel='#8d776b'; face='#aa9687'; top='#b49f8e'; bottom='#9d8779'}
)
function Chamfer($inset,$cut,$color){
    $l=$inset; $r=36-$inset
    Poly @(($l+$cut),$l,($r-$cut),$l,$r,($l+$cut),$r,($r-$cut),($r-$cut),$r,($l+$cut),$r,$l,($r-$cut),$l,($l+$cut)) $color
}
foreach($button in $buttons){
    $bitmap=[Drawing.Bitmap]::new(36,36)
    $g=[Drawing.Graphics]::FromImage($bitmap)
    Chamfer 0 4 $button.outer
    Chamfer 1 4 $button.rim
    Chamfer 3 3 $button.bevel
    Chamfer 4 3 $button.face
    Rect 7 4 22 1 $button.top
    Rect 7 31 22 1 $button.bottom
    $g.Dispose()
    if($bitmap.GetPixel(0,0).A -ne 0 -or $bitmap.GetPixel(18,18).A -ne 255){
        throw "Unexpected alpha in $($button.id)"
    }
    $bitmap.Save((Join-Path $sprites "button-$($button.id).png"),[Drawing.Imaging.ImageFormat]::Png)
    $bitmap.Dispose()
}
