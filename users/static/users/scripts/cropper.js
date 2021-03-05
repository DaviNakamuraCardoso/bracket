/*
* cropper.js -- v0.1
* Copyright 2012 Oscar Key
* A simple image cropping library which uses pure Javascript and the <canvas> tag in order to crop images in the browser.
*/

/*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
const COLORS = {
	white: "#ffffff",
	black: "#000000",
	overlay: "rgba(0, 0, 0, 0.6)"
};

class Canvas
{
	constructor(element)
	{
		this.element = element;
		this.image;
		this.restoreImage;
		this.cropping = false;
		this.context = this.element.getContext("2d");
		this.currentDimens = {};
		this.overlay =
		{
			x: 50,
			y: 50,
			width: 400,
			height: 400,
			resizerSide: 10,
			ratioXY: 1
		};
		this.drag = {
			type: "", // options: "moveOverlay", "resizeOverlay"
			inProgress: false,
			originalOverlayX: 0,
			originalOverlayY: 0,
			originalX: 0,
			originalY: 0,
			originalOverlayWidth: 0,
			originalOverlayHeight: 0
		};

	};

	start()
	{
		// only continue if an image is loaded
		if(this.image === undefined) {
			return false;
		}

		// save the current state
		this.restoreImage = new Image();
		this.restoreImage.src = this.image.src;

		cropping = true;
		this.draw();


		return true;
	};

	draw()
	{
		// clear the canvas
		this.context.clearRect(0, 0, canvas.width, canvas.height);

		// if we don't have an image file, abort the draw at this point
		if(this.image === undefined) {
			return;
		}

		// draw the image
		let dimens = this.currentDimens;
		this.context.drawImage(image, 0, 0, dimens.width, dimens.height);

		// draw cropping stuff if we are cropping
		if(cropping) {
			// draw the overlay
			drawOverlay();

			// draw the resizer
			let x = overlay.x + overlay.width - 5,
			y = overlay.y + overlay.height - 5,
			w = overlay.resizerSide,
			h = overlay.resizerSide;

			context.save();
			context.fillStyle = COLORS.black;
			context.strokeStyle = COLORS.white;
			context.fillRect(x, y, w, h);
			context.strokeRect(x, y, w, h);
			context.restore();
		}
	}

	drawOverlay() {
		// draw the overlay using a path made of 4 trapeziums (ahem)
		this.context.save();

		this.context.fillStyle = COLORS.overlay;
		this.context.beginPath();
		this.context.moveTo(0, 0);
		this.context.lineTo(overlay.x, overlay.y);
		this.context.lineTo(overlay.x + overlay.width, overlay.y);
		this.context.lineTo(canvas.width, 0);
		this.context.moveTo(canvas.width, 0);
		this.context.lineTo(overlay.x + overlay.width, overlay.y);
		this.context.lineTo(overlay.x + overlay.width, overlay.y + overlay.height);
		this.context.lineTo(canvas.width, canvas.height);
		this.context.moveTo(canvas.width, canvas.height);
		this.context.lineTo(overlay.x + overlay.width, overlay.y + overlay.height);
		this.context.lineTo(overlay.x, overlay.y + overlay.height);
		this.context.lineTo(0, canvas.height);
		this.context.moveTo(0, canvas.height);
		this.context.lineTo(overlay.x, overlay.y + overlay.height);
		this.context.lineTo(overlay.x, overlay.y);
		this.context.lineTo(0, 0);

		this.context.fill();
		this.context.restore();
	}

	setRatio(ratio) {
		this.overlay.ratioXY = ratio;
		this.overlay.height = Math.floor(this.overlay.width * ratio);
	}
	getScaledImageDimensions(width, height) {
		// choose the dimension to scale to, depending on which is "more too big"
		let factor = 1;
		if((this.element.width - width) < (this.element.height - height)) {
			// scale to width
			factor = this.element.width / width;
		} else {
			// scale to height
			factor = this.element.height / height;
		}
		// important "if,else" not "if,if" otherwise 1:1 images don't scale

		let dimens = {
			width: Math.floor(width * factor),
			height: Math.floor(height * factor),
			factor: factor
		};

		return dimens;
	}
	getTouchPos(touchEvent) {
		let rect = this.element.getBoundingClientRect();

		return {
			x: touchEvent.touches[0].clientX - rect.left,
			y: touchEvent.touches[0].clientY - rect.top
		};
	}
	/**
	* @param {Number} x position mouse / touch client event
	* @param {Number} y position mouse / touch client event
	*/
	getClickPos({x, y}) {
		return {
			x : x - window.scrollX,
			y : y - window.scrollY
		}
	}
	isInOverlay(x, y) {
		return x > this.overlay.x && x < (this.overlay.x + this.overlay.width) && y > this.overlay.y && y < (this.overlay.y + this.overlay.height);
	}

	isInHandle(x, y) {
		return x > (this.overlay.x + this.overlay.width - this.overlay.resizerSide) && x < (this.overlay.x + this.overlay.width + this.overlay.resizerSide) && y > (this.overlay.y + this.overlay.height - this.overlay.resizerSide) && y < (this.overlay.y + this.overlay.height + this.overlay.resizerSide);
	}

}

function start(canvas) {
	"use strict"; // helps us catch otherwise tricky bugs










	/* EVENT LISTENER STUFF */


	/**
	* @param {Number} x position mouse / touch client event
	* @param {Number} y position mouse / touch client event
	*/
	function initialCropOrMoveEvent({x, y}) {
		// if the mouse clicked in the overlay
		if(isInOverlay(x, y)) {
			drag.type = "moveOverlay";
			drag.inProgress = true;
			drag.originalOverlayX = x - overlay.x;
			drag.originalOverlayY = y - overlay.y;
		}

		if(isInHandle(x, y)) {
			drag.type = "resizeOverlay";
			drag.inProgress = true;
			drag.originalX = x;
			drag.originalY = y;
			drag.originalOverlayWidth = overlay.width;
			drag.originalOverlayHeight = overlay.height;
		}
	}

	/**
	* @param {Number} x horizontal position mouse or touch event
	* @param {Number} y vertical position mour or touch event
	* @description this function will be crop image inside canvas
	*/
	function startCropOrMoveEvent({x, y}) {

		// Set current cursor as appropriate
		if(isInHandle(x, y) || (drag.inProgress && drag.type === "resizeOverlay")) {
			canvas.style.cursor = 'nwse-resize'
		} else if(isInOverlay(x, y)) {
			canvas.style.cursor = 'move'
		} else {
			canvas.style.cursor = 'auto'
		}

		// give up if there is no drag in progress
		if(!drag.inProgress) {
			return;
		}

		// check what type of drag to do
		if(drag.type === "moveOverlay") {
			overlay.x = x - drag.originalOverlayX;
			overlay.y = y - drag.originalOverlayY;
			// Limit to size of canvas.
			let xMax = canvas.width - overlay.width;
			let yMax = canvas.height - overlay.height;

			if(overlay.x < 0) {
				overlay.x = 0;
			} else if(overlay.x > xMax) {
				overlay.x = xMax;
			}

			if(overlay.y < 0) {
				overlay.y = 0;
			} else if(overlay.y > yMax) {
				overlay.y = yMax;
			}

			draw();
		} else if(drag.type === "resizeOverlay") {
			overlay.width = drag.originalOverlayWidth + (x - drag.originalX);

			// do not allow the overlay to get too small
			if(overlay.width < 10) {
				overlay.width = 10;
			}

			// Don't allow crop to overflow
			if(overlay.x + overlay.width > canvas.width) {
				overlay.width = canvas.width - overlay.x;
			}

			overlay.height = overlay.width * overlay.ratioXY;

			if(overlay.y + overlay.height > canvas.height) {
				overlay.height = canvas.height - overlay.y;
				overlay.width = overlay.height / overlay.ratioXY;
			}

			draw();
		}
	}

	function addEventListeners() {
		// add mouse listeners to the canvas
		canvas.onmousedown = function(event) {
			// depending on where the mouse has clicked, choose which type of event to fire
			let coords = canvas.getMouseCoords(event);
			initialCropOrMoveEvent(getClickPos(coords));
		};

		canvas.onmouseup = function(event) {
			// cancel any drags
			drag.inProgress = false;
		};

		canvas.onmouseout = function(event) {
			// cancel any drags
			drag.inProgress = false;
		};

		canvas.onmousemove = function(event) {
			let coords = canvas.getMouseCoords(event);

			startCropOrMoveEvent(getClickPos(coords));
		};

		canvas.addEventListener('touchstart', event => {
			initialCropOrMoveEvent(getTouchPos(event));
		});

		canvas.addEventListener('touchmove', event => {
			startCropOrMoveEvent(getTouchPos(event));
		});

		canvas.addEventListener('touchend', event => {
			drag.inProgress = false;
		})
	}


	/* CROPPING FUNCTIONS */
	function cropImage(entire) {
		// if we don't have an image file, abort at this point
		if(image === undefined) {
			return false;
		}

		// if we aren't cropping, ensure entire is tru
		if(!cropping) {
			entire = true;
		}

		// assume we want to crop the entire image, this will be overriden below
		let x = 0;
		let y = 0;
		let width = image.width;
		let height = image.height;

		if(!entire) {
			// work out the actual dimensions that need cropping
			let factor = currentDimens.factor;
			x = Math.floor(overlay.x / factor);
			y = Math.floor(overlay.y / factor);
			width = Math.floor(overlay.width / factor);
			height = Math.floor(overlay.height / factor);

			// check the values are within range of the image
			if(x < 0){ x = 0; }
			if(x > image.width){ x = image.width; }
			if(y < 0){ y = 0; }
			if(y > image.height){ y = image.height; }

			if(x + width > image.width){ width = image.width - x; }
			if(y + height > image.height){ height = image.height - y; }
		}

		// load the image into the cropping canvas
		let cropCanvas = document.createElement("canvas");
		cropCanvas.setAttribute("width", width);
		cropCanvas.setAttribute("height", height);

		let cropContext = cropCanvas.getContext("2d");
		cropContext.drawImage(image, x, y, width, height, 0, 0, width, height);

		return cropCanvas;
	}

	/* function borrowed from http://stackoverflow.com/a/7261048/425197 */
	function dataUrlToBlob(dataURI) {
		// convert base64 to raw binary data held in a string
		let byteString = atob(dataURI.split(',')[1]);

		// separate out the mime component
		let mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

		// write the bytes of the string to an ArrayBuffer
		let ab = new ArrayBuffer(byteString.length);
		let ia = new Uint8Array(ab);
		for (let i = 0; i < byteString.length; i++) {
			ia[i] = byteString.charCodeAt(i);
		}

		// write the ArrayBuffer to a blob, and you're done
		return new Blob([ia], {type: mimeString});
	}

	/* API FUNCTIONS */
	cropper.showImage = function(src) {
		cropping = false;
		image = new Image();
		image.onload = function() {

			currentDimens = getScaledImageDimensions(image.width, image.height) ; // work out the scaling
			draw();
		};
		image.src = src;
	};



	cropper.getCroppedImageSrc = function() {
		if(image) {
			// return the cropped image
			let cropCanvas = cropImage(!cropping); // cropping here controls if we get the entire image or not, desirable if the user is not cropping
			let url = cropCanvas.toDataURL("png");

			let valueSize = (overlay.width * image.width / currentDimens.width);
			let valueX = (overlay.x * image.width / currentDimens.width);
			let valueY = (overlay.y * image.height / currentDimens.height);

			console.log(valueSize);
			console.log(valueX);
			console.log(valueY);

			const canvasDiv = canvas.parentElement;

			canvasDiv.querySelector(".size").value = Math.round(valueSize);
			canvasDiv.querySelector(".picture-x").value = Math.round(valueX);
			canvasDiv.querySelector(".picture-y").value = Math.round(valueY);

			// show the new image, only bother doing this if it isn't already displayed, ie, we are cropping
			if(cropping) {
				cropper.showImage(url);
			}

			cropping = false;
			return url;
		} else {
			return false;
		}
	};

	cropper.getCroppedImageBlob = function(type) {
		if(image) {
			// return the cropped image
			let cropCanvas = cropImage(!cropping); // cropping here controls if we get the entire image or not, desirable if the user is not cropping
			let url = cropCanvas.toDataURL(type || "png");

			// show the new image, only bother doing this if it isn't already displayed, ie, we are cropping
			if(cropping) {
				cropper.showImage(url);
			}

			cropping = false;

			// convert the url to a blob and return it
			return dataUrlToBlob(url);
		} else {
			return false;
		}
	};

	cropper.start = function(newCanvas, ratio) {
		// get the context from the given canvas
		canvas = newCanvas;
		if(!canvas.getContext) {
			return; // give up
		}
		context = canvas.getContext("2d");

		// Set default overlay position
		overlay =
		// set up the overlay ratio
		if(ratio) {
			setRatio(ratio);
		}

		// setup mouse stuff
		addEventListeners();
	};

	cropper.restore = function() {
		if(restoreImage === undefined) {
			return false;
		}

		cropping = false;

		// show the saved image
		cropper.showImage(restoreImage.src);
		cropper.startCropping();
		return true;
	};


	/* modify the canvas prototype to allow us to get x and y mouse coords from it */
	HTMLCanvasElement.prototype.getMouseCoords = function(event){
		// loop through this element and all its parents to get the total offset
		let totalOffsetX = 0;
		let totalOffsetY = 0;
		let canvasX = 0;
		let canvasY = 0;
		let currentElement = this;

		do {
			totalOffsetX += currentElement.offsetLeft;
			totalOffsetY += currentElement.offsetTop;
		}
		while(currentElement = currentElement.offsetParent)

		canvasX = event.pageX - totalOffsetX;
		canvasY = event.pageY - totalOffsetY + window.scrollY;


		return {x:canvasX, y:canvasY}
	}


}(window.cropper = window.cropper || {}));


export default function updateCanvas()
{
	const canvases = document.querySelectorAll('.canvas');

	canvases.forEach(canvas => {
		cropper.start(canvas, 1);

		let canvasDiv = canvas.parentElement;
    	const input  = canvasDiv.querySelector(".fileInput");


		input.onchange = () => {
			// this function will be called when the file input below is changed
			let file = input.files[0];  // get a reference to the selected file

			let reader = new FileReader(); // create a file reader
			// set an onload function to show the image in cropper once it has been loaded
			reader.onload = function(event) {
				let data = event.target.result; // the "data url" of the image
				cropper.showImage(data); // hand this to cropper, it will be displayed
				cropper.startCropping();
			};

			reader.readAsDataURL(file); // this loads the file as a data url calling the function above once done

		}
		const crop = canvasDiv.querySelector(".crop");
		const restore = canvasDiv.querySelector(".restore");

		crop.onclick = () => {
			cropper.getCroppedImageSrc();
		}

		restore.onclick = () => {
			cropper.restore();
		}

	});

}
