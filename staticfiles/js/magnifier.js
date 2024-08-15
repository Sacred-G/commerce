document.addEventListener('DOMContentLoaded', function() {
  const magnifierContainer = document.querySelector('.image-magnifier-container');
  const magnifier = magnifierContainer.querySelector('.image-magnifier');
  const img = magnifier.querySelector('.magnifier-img');
  const lens = magnifier.querySelector('.magnifier-lens');
  const toggleBtn = magnifierContainer.querySelector('.magnifier-toggle');

  let isActive = false;

  toggleBtn.addEventListener('click', function() {
    isActive = !isActive;
    magnifier.classList.toggle('active');
    this.textContent = isActive ? 'Disable Magnifier' : 'Enable Magnifier';
    if (!isActive) {
      hideLens();
    }
  });

  magnifier.addEventListener('mousemove', magnify);
  magnifier.addEventListener('mouseenter', showLens);
  magnifier.addEventListener('mouseleave', hideLens);

  function magnify(event) {
    if (!isActive) return;
    const rect = magnifier.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    let lensSize = 300; // Adjust this value to change the size of the magnifying lens
    lens.style.width = lens.style.height = `${lensSize}px`;
    lens.style.left = `${x - lensSize / 2}px`;
    lens.style.top = `${y - lensSize / 2}px`;

    let zoom = 2; // Adjust this value to change the zoom level
    lens.style.backgroundImage = `url('${img.src}')`;
    lens.style.backgroundSize = `${img.width * zoom}px ${img.height * zoom}px`;
    lens.style.backgroundPosition = `-${x * zoom - lensSize / 2}px -${y * zoom - lensSize / 2}px`;
  }

  function showLens() {
    if (isActive) {
      lens.style.opacity = 1;
    }
  }

  function hideLens() {
    lens.style.opacity = 0;
  }
});
