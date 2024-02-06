// سایت روی اکانت های دیگه بخش ارسال درخواست به دیتابیس برای تغییر وضعیت سنسور ها اررور میده.


var token = document.getElementById('token').getAttribute('data-token');
var email = document.getElementById('email').getAttribute('data-email');
var phone = document.getElementById('phone').getAttribute('data-phone');
var name = document.getElementById('name').getAttribute('data-name');
console.log(token, email, phone);
document.addEventListener('DOMContentLoaded', function () {
  sendRequestToDatabase();
});

function sendRequestToDatabase() {
  // مسیر و تنظیمات دیگر درخواست را تنظیم کنید
  var data = {
    token: token
  };
  const apiData = 'http://127.0.0.1:5000/api/data'; //api/end-point
  const requestOptions = {
      method: 'POST', // یا 'GET' یا هر متدی که نیاز دارید
      headers: {
          'Content-Type': 'application/json', // در صورت نیاز
      },
      // محتوای درخواست را اگر نیاز دارید تنظیم کنید
      body: JSON.stringify(data)
  };
  // ارسال درخواست با استفاده از fetch
  fetch(apiData, requestOptions)
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
      })
      .then(data => {
          if (data.strike === "1") {
            document.getElementById("strikeSensor").classList.add("active");
          } else {
            document.getElementById("strikeSensor").classList.remove("active");
          }
          if (data.saving === "1") {
            document.getElementById("batterysensor").classList.add("active");
          } else {
            document.getElementById("batterysensor").classList.remove("active");
          }
          if (data.pir === "1") {
            document.getElementById("pirSensor").classList.add("active");
          } else {
            document.getElementById("pirSensor").classList.remove("active");
          }
          if (data.temp === "1"){
            document.getElementById("tempSensor").classList.add("active");
            if (data.temperature === "0") {
              document.getElementById("tempSensor2").classList.remove("active");
            } else {
              document.getElementById("tempSensor2").classList.add("active");
              const dataHTML = data.temperature+"C";
              document.getElementById("DataTemp").innerHTML = dataHTML;
              document.getElementById("DataTemp1").innerHTML = dataHTML;
            }
          } else {
            document.getElementById("tempSensor").classList.remove("active");
          }
      })
      .catch(error => console.error('Error sending request:', error));
}


function updateText() {
  const switchInput = document.getElementById("pir");
  const statusText = document.getElementById("status-text-pir");

  statusText.textContent = switchInput.checked ? "OFF" : "ON";
  if (switchInput.checked){
    var StatusPIR = {
      token: token,
      pir: "0"
    };
    const apiPIR = "/api/status";
    const requestsStatus = {
      method: "POST",
      headers: {
          'Content-Type': 'application/json', // در صورت نیاز
      },
      body: JSON.stringify(StatusPIR)
    }
    fetch(apiPIR, requestsStatus)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
          if (data === "Data Manual Save"){
            console.log("Status Sensor PIR : OFF")
          }
        })
        .catch(error => console.error('Error sending request:', error));
  } else {
    var StatusPIR = {
      token: token,
      pir: "1"
    };
    const apiPIR = "/api/status";
    const requestsStatus = {
      method: "POST",
      headers: {
          'Content-Type': 'application/json', // در صورت نیاز
      },
      body: JSON.stringify(StatusPIR)
    }
    changeColor('frame1');
    fetch(apiPIR, requestsStatus)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
          if (data === "Data Manual Save"){
            console.log("Status Sensor PIR : ON")
          }
        })
        .catch(error => console.error('Error sending request:', error));
  }
}

function updateText1() {
    const switchInput = document.getElementById("sensor");
    const statusText = document.getElementById("status-text-sensor");
  
    statusText.textContent = switchInput.checked ? "OFF" : "ON";
    if (switchInput.checked){
      var StatusPIR = {
        token: token,
        strike: "0"
      };
      const apiPIR = "/api/status";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      };
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : OFF")
            }
          })
          .catch(error => console.error('Error sending request:', error));
    } else {
      var StatusPIR = {
        token: token,
        strike: "1"
      };
      const apiPIR = "/api/status";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      changeColor('frame2');
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : ON")
            }
          })
          .catch(error => console.error('Error sending request:', error));
  }

}
function updateText2() {
    const switchInput = document.getElementById("temp");
    const statusText = document.getElementById("status-text-temp");
  
    statusText.textContent = switchInput.checked ? "OFF" : "ON";
    if (switchInput.checked){
      var StatusPIR = {
        token: token,
        temp: "0"
      };
      const apiPIR = "/api/status";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : OFF")
            }
          })
          .catch(error => console.error('Error sending request:', error));
    } else {
      var StatusPIR = {
        token: token,
        temp: "1"
      };
      const apiPIR = "/api/status";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      changeColor('frame3');
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : ON")
            }
          })
          .catch(error => console.error('Error sending request:', error));
  }
}
function updateText3() {
    const switchInput = document.getElementById("lamp");
    const statusText = document.getElementById("status-text-lamp");
  
    statusText.textContent = switchInput.checked ? "OFF" : "ON";
    if (switchInput.checked){
      var StatusPIR = {
        token: token,
        lamps: "0"
      };
      const apiPIR = "/api/status";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : OFF")
            }
          })
          .catch(error => console.error('Error sending request:', error));
    } else {
      var StatusPIR = {
        token: token,
        lamps: "1"
      };
      const apiPIR = "/api/status";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      changeColor('frame4');
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : ON")
            }
          })
          .catch(error => console.error('Error sending request:', error));
  }
}


function updateText4() {
    const switchInput = document.getElementById("gmail");
    if (switchInput.checked){
      var StatusPIR = {
        token: token,
        email: "0"
      };
      const apiPIR = "/api/notification";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : OFF")
            }
          })
          .catch(error => console.error('Error sending request:', error));
    } else {
      var StatusPIR = {
        token: token,
        email: "1"
      };
      const apiPIR = "/api/notification";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      changeColor('frame4');
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : ON")
            }
          })
          .catch(error => console.error('Error sending request:', error));
  }
}

function updateText5() {
    const switchInput = document.getElementById("telegram");
    if (switchInput.checked){
      var StatusPIR = {
        token: token,
        telegram: "0"
      };
      const apiPIR = "/api/notification";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : OFF")
            }
          })
          .catch(error => console.error('Error sending request:', error));
    } else {
      var StatusPIR = {
        token: token,
        telegram: "1"
      };
      const apiPIR = "/api/notification";
      const requestsStatus = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', // در صورت نیاز
        },
        body: JSON.stringify(StatusPIR)
      }
      changeColor('frame4');
      fetch(apiPIR, requestsStatus)
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(data => {
            if (data === "Data Manual Save"){
              console.log("Status Sensor PIR : ON")
            }
          })
          .catch(error => console.error('Error sending request:', error));
  }
}

// script.js


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

async function logout() {
  console.log("logout");
  try {
      const response = await fetch('http://127.0.0.1:5000/logout', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          },
      });
      console.log(response.status);
  } catch (error) {
      console.error('Error:', error);
  }
}

function changeFrame(frameNumber) {
  const frames = document.querySelectorAll('.frameleft');
  
  frames.forEach((frame, index) => {
      if (index + 1 === frameNumber) {
          frame.style.display = 'block';
      } else {
          frame.style.display = 'none';
      }
      if (index + 1 == frameNumber && index + 1 == 7) {
        logout();
      }
  });
}


function sendData() {
  const data = {
      key1: 'value1',
      key2: 'value2'
      // Add more key-value pairs as needed
  };

  fetch('https://example.com/api', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
          // Add other headers if needed
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      // Do something with the response data if needed
  })
  .catch((error) => {
      console.error('Error:', error);
      // Handle errors here
  });
}
