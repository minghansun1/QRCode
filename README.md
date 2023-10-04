# QRCode
A tool that can find cut up pieces of a QR code in an image and piece them together to form a readable code. Uses OpenCV and image-straightening algorithms to find the correct orientation and position of each component of a qr code.

There are 4 main components to this project: 
1) Find each piece of the QR code (work in progress)
2) Rotate each piece so that all lines are horizontal or vertical (bound method and rotate method)
3) Create every possible arrangement of QR code pieces and attempt to read the arrangement (try_all method)

