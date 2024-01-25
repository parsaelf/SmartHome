function updateText() {
    const switchInput = document.getElementById("pir");
    const statusText = document.getElementById("status-text");
  
    statusText.textContent = switchInput.checked ? "OFF" : "ON";
}
function updateText1() {
    const switchInput = document.getElementById("sensor");
    const statusText = document.getElementById("status-text-sensor");
  
    statusText.textContent = switchInput.checked ? "OFF" : "ON";
}
function updateText2() {
    const switchInput = document.getElementById("temp");
    const statusText = document.getElementById("status-text-temp");
  
    statusText.textContent = switchInput.checked ? "OFF" : "ON";
}
function updateText3() {
    const switchInput = document.getElementById("lamp");
    const statusText = document.getElementById("status-text-lamp");
  
    statusText.textContent = switchInput.checked ? "OFF" : "ON";
}
function updateText4() {
  const switchInput = document.getElementById("sensor");
  const statusText = document.getElementById("status-text-sensor");

  statusText.textContent = switchInput.checked ? "OFF" : "ON";
}
// script.js
document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('pir');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('PIR is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('sensor');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('Strike Sensor is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('temp');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('Temp Sensor is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('lamp');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('lamp is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('pir2');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('PIR is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('sen2');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('Strike Sensor is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('router');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('Router is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const switchInput = document.getElementById('power');
  
    switchInput.addEventListener('change', function () {
      // Do something when the switch state changes
      console.log('Power Saving is now ' + (this.checked ? 'ON' : 'OFF'));
    });
});


function changeColor(frameId) {
    const frame = document.getElementById(frameId);
    frame.classList.toggle('clicked');
}

function changeFrame(frameNumber) {
  const frames = document.querySelectorAll('.frameleft');
  
  frames.forEach((frame, index) => {
      if (index + 1 === frameNumber) {
          frame.style.display = 'block';
      } else {
          frame.style.display = 'none';
      }
  });
}
