// list of sounds
const sound = {
  65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
  87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
  83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
  69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
  68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
  70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
  84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
  71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
  89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
  72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
  85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
  74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
  75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
  79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
  76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
  80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
  186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

// for key hover effect
let whiteKeys = document.querySelectorAll('.white-key');
let blackKeys = document.querySelectorAll('.black-key');
let allKeys = [...blackKeys, ...whiteKeys];

allKeys.forEach((pianoKey) => {
  pianoKey.addEventListener('mouseover', (e) => {
      allKeys.forEach(pKey => pKey.classList.add('key-hover'));
      // remove text after certain 1500 ms
      window.setTimeout(() => allKeys.forEach(pKey => pKey.classList.remove('key-hover')), 1500)
  });
});


let aSource = document.querySelectorAll('.audio_source');
let disablePiano = false;
let seq = "";

// handling key press events ONLY for VALID KEYS
window.addEventListener('keydown', (e) => {
  if (disablePiano || e.isComposing || e.keyCode === 229) {
      return;
  }

  if (!Object.keys(sound).includes(`${e.keyCode}`)) {
      return;
  }

  // USING UPPER SO ASCCI VALUES CORRESPOND
  let keyID = `key-${e.key.toUpperCase()}`;
  if (e.key == ';') {
      keyID = "key-SColon";
  }

  // if key pressed shrink the key and change color
  document.getElementById(keyID).classList.add('key-click');

  // will return to normal height and color after 500
  setTimeout(() => {
      document.getElementById(keyID).classList.remove('key-click');
  }, 500);

  ///play multiple keys at the same time
  let i = 0;
  while (i < aSource.length) {
      if (aSource[i].ended) {
          aSource[i].src = sound[e.keyCode];
          aSource[i].play();
          break;
      }
      i++;
  }

  if (i == aSource.length) {
      aSource[0].src = sound[e.keyCode];
      aSource[0].play();
  }
  // remove the first letter if  length of  sequence is equal to  length of 'weseeyou' 
  if (seq.length >= 8) {
      seq = seq.slice(1, 8);
  }

  seq += e.key;

  // if 'weseeyou' is the sequence, disable the piano & replace the background
  if (seq.toLowerCase() == "weseeyou") {
      disablePiano = true;
      document.querySelector('.piano').classList.add('weseeyou');
      document.querySelector('.key-container').classList.add('weseeyou');
      document.querySelector('.poem-text').classList.add('weseeyou');
      document.querySelector('.key-container').classList.add('weseeyou');
      document.querySelector('#scary_audio').play();
  }
});