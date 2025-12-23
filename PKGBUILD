pkgname=trackdown
pkgver=1.0.0
pkgrel=1
pkgdesc="Modern GUI application to download Spotify tracks"
arch=('any')
url="https://example.com/trackdown"
license=('MIT')

depends=('python' 'python-pyqt6')

optdepends=(
  'python-spotdl: Spotify downloading backend'
)


source=("trackdown-src.tar.gz")
sha256sums=('SKIP')

package() {
  cd "$srcdir/trackdown-src"

  # launcher
  install -Dm755 trackdown.sh \
    "$pkgdir/usr/bin/trackdown"

  # create app directory
  install -d "$pkgdir/usr/lib/trackdown"

  # app source files
  install -Dm644 app/*.py \
    "$pkgdir/usr/lib/trackdown/"

  # icon
  install -Dm644 app/assets/trackdown.png \
    "$pkgdir/usr/share/icons/hicolor/256x256/apps/trackdown.png"

  # desktop entry
  install -Dm644 trackdown.desktop \
    "$pkgdir/usr/share/applications/trackdown.desktop"
}

