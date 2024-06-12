window.addEventListener('scroll', () => {
    const yOffset = window.pageYOffset; // 获取页面向下滚动的距离
    // 将偏移值发送到外部窗口
    window.parent.postMessage({yOffset}, '*'); // '*' 表示发送到所有窗口，可以根据需要更改目标窗口
});

document.addEventListener("DOMContentLoaded", function() {
  // 在文档加载完成后执行您的代码
  const documentWidth = Math.max(
    document.body.scrollWidth, document.documentElement.scrollWidth,
    document.body.offsetWidth, document.documentElement.offsetWidth,
    document.body.clientWidth, document.documentElement.clientWidth
  );

  const documentHeight = Math.max(
    document.body.scrollHeight, document.documentElement.scrollHeight,
    document.body.offsetHeight, document.documentElement.offsetHeight,
    document.body.clientHeight, document.documentElement.clientHeight
  );

  console.log('文档宽度:', documentWidth);
  console.log('文档高度:', documentHeight);
});

