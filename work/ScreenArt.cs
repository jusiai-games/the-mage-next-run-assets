using System.Collections.Generic;
using TheMageNextRun.Spells;
using UnityEngine;
using UnityEngine.UI;

namespace TheMageNextRun.Screens
{
    internal static class ScreenArt
    {
        internal static readonly Color32 Ink = new(255, 243, 218, 255);

        private static readonly Dictionary<Element, Sprite> Cards = new();

        internal static Sprite Card(Element element)
        {
            if (!Cards.TryGetValue(element, out var sprite))
            {
                sprite = Resources.Load<Sprite>($"SpellsToGo/Card{element}");
                Cards.Add(element, sprite);
            }

            return sprite;
        }

        internal static void Frame(GameObject panel)
        {
            if (panel.TryGetComponent<Image>(out var image))
            {
                var sprite = Resources.Load<Sprite>("SpellsToGo/DialogPanel");
                if (sprite != null)
                {
                    image.sprite = sprite;
                    image.type = Image.Type.Sliced;
                    image.color = Color.white;
                }
            }
        }

        internal static void Outline(Text label)
        {
            if (label == null)
            {
                return;
            }

            label.color = Ink;
            if (!label.TryGetComponent<Outline>(out var outline))
            {
                outline = label.gameObject.AddComponent<Outline>();
            }

            outline.effectColor = new Color32(26, 28, 44, 242);
            outline.effectDistance = new Vector2(1.5f, -1.5f);
        }

        internal static void PrimaryButton(Button button)
        {
            var label = button.GetComponentInChildren<Text>(true);
            Outline(label);
            if (button.transition == Selectable.Transition.ColorTint)
            {
                var colors = button.colors;
                colors.normalColor = new Color32(255, 225, 184, 255);
                colors.highlightedColor = Color.white;
                colors.pressedColor = new Color32(196, 169, 153, 255);
                colors.selectedColor = new Color32(255, 238, 209, 255);
                colors.disabledColor = new Color32(135, 134, 152, 255);
                button.colors = colors;
            }
        }
    }
}
