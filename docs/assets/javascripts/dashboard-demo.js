// Scale each embedded Catalogue Dashboard page from its 1280-pixel Power BI width.
document.querySelectorAll(".dashboard-demo").forEach(function (frame) {
  new ResizeObserver(function () {
    frame.style.setProperty("--dashboard-scale", frame.clientWidth / 1280);
    frame.classList.add("is-scaled");
  }).observe(frame);
});
