from decimal import Decimal
import qrcode.image.base
import qrcode.image.svg

class BoxesQrCodeFactory(qrcode.image.base.BaseImage):
    """
    SVG image builder
    Creates a QR-code image as a SVG document fragment.
    """
    _SVG_namespace = "http://www.w3.org/2000/svg"
    kind = "SVG"
    allowed_kinds = ("SVG",)

    def __init__(self, *args, ctx=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        # Save the unit size, for example the default box_size of 10 is '1mm'.
        self.unit_size = self.units(self.box_size)

    def drawrect(self, row, col):
        self.ctx.rectangle(*self._rect(row, col))
        self._img.append(self._rect(row, col))

    def units(self, pixels, text=True):
        """
        A box_size of 10 (default) equals 1mm.
        """
        units = Decimal(pixels) / 10
        if not text:
            return units
        return '%smm' % units

    def save(self, stream, kind=None):
        self.check_kind(kind=kind)
        self._write(stream)

    def to_string(self):
        return f"".join(self._img)

    def new_image(self, **kwargs):
        self._img = []
        return self._img

    def _rect(self, row, col):
        x, y = row, col
        x, y = float(x), float(y)
        w, h = float(1), float(1)
        return x, y, w, h

    def _write(self, stream):
        stream.write("".join(self._img))

if __name__=="__main__":
    import qrcode
    import qrcode.image
    q = qrcode.QRCode(image_factory=BoxesQrCodeFactory, box_size=10)
    q.add_data('hello')
    ctx = "a context"
    img = q.make_image(ctx="a context")
    print(img.to_string())
