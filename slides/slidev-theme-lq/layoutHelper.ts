import type { CSSProperties } from 'vue'

/**
 * Resolve urls from frontmatter and append with the base url
 */
export function resolveAssetUrl(url: string) {
  return url
}


export function handleBackground(background?: string, dim = false): CSSProperties {
  const isColor =
    background &&
    ['#', 'rgb', 'hsl'].some(prefix => background.indexOf(prefix) === 0)

  // Consistently create the background style for images:
  const backgroundImage = !isColor && background
    ? dim
      ? `linear-gradient(#0005, #0008), url(${resolveAssetUrl(background)})`
      : `url(${resolveAssetUrl(background)})`
    : undefined

  const style: CSSProperties = {
    // When using a color as background
    background: isColor ? background : undefined,
    // Optionally change text color if an image background is set
    color: background && !isColor ? 'white' : undefined,
    // Only use backgroundImage for image backgrounds
    backgroundImage,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    backgroundSize: 'cover'
  }

  // If background wasn't set, remove the property
  if (!style.background) {
    delete style.background
  }

  return style
}

