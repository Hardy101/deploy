let scrolling = false; // Flag to track if smooth scrolling is in progress
let scrollTimeout; // Timeout letiable for gradual stop effect

// Smooth scroll when the down arrow or spacebar is pressed
function smoothScroll() {
  if (scrolling) return; // Don't trigger smooth scroll if already scrolling

  scrolling = true;

  let currentPosition = window.scrollY;
  let windowHeight = window.innerHeight;
  let documentHeight = document.documentElement.scrollHeight;

  // Calculate the new scroll position
  let newPosition = currentPosition + windowHeight;

  // Calculate the duration for smooth scrolling (adjust as needed)
  let duration = 800; // 800 milliseconds

  // Calculate the distance to scroll per frame
  let distance = Math.abs(newPosition - currentPosition);
  let frames = 60; // Number of frames for smooth scrolling
  let distancePerFrame = distance / frames;

  let currentFrame = 0;

  function scrollStep() {
    currentFrame++;
    let scrollAmount;

    if (currentFrame === frames) {
      // Stop scrolling when reaching the final frame
      scrollAmount = newPosition;
      scrolling = false;
    } else {
      // Calculate the scroll position for the current frame
      let progress = currentFrame / frames;
      scrollAmount = currentPosition + distancePerFrame * progress;
    }

    // Scroll to the new position for this frame
    window.scrollTo({
      top: scrollAmount,
      behavior: "auto", // Use "auto" for smoother effect
    });

    // Continue scrolling until the final frame is reached
    if (currentFrame < frames) {
      requestAnimationFrame(scrollStep);
    }
  }

  // Start smooth scrolling animation
  scrollStep();
}

// Smooth scroll when the down arrow or spacebar is pressed
function handleKeyPress(event) {
  if (event.code === "Space" || event.code === "ArrowDown") {
    event.preventDefault(); // Prevent the default behavior of scrolling
    smoothScroll();
  }
}

// Gradual stop effect when scrolling is released
function handleScrollRelease() {
  clearTimeout(scrollTimeout);

  if (!scrolling) {
    scrollTimeout = setTimeout(function () {
      window.scrollTo({
        top: Math.round(window.scrollY),
        behavior: "smooth",
      });
    }, 100); // Adjust the delay as needed (in milliseconds)
  }
}

// Attach event listeners
document.addEventListener("keydown", handleKeyPress);
document.addEventListener("wheel", handleScrollRelease, { passive: true });
