document.addEventListener('DOMContentLoaded', function () {
    let figure = document.getElementById('image');
  
    directions.addEventListener('change', function () {
      figure.setAttribute('tooltip-dir', this.value);
    });
  });