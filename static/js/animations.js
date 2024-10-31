document.addEventListener('DOMContentLoaded', function () {
	const fadeInBlocks = document.querySelectorAll('.fade-in-block');

	function handleScroll() {
		fadeInBlocks.forEach(block => {
			const blockPosition = block.getBoundingClientRect().top;
			const windowHeight = window.innerHeight;

			// Проверяем, виден ли блок на экране
			if (blockPosition < windowHeight - 39) {
				block.classList.add('visible');
			}
		});
	}

	// Выполняем проверку при прокрутке
	window.addEventListener('scroll', handleScroll);

	// Выполняем проверку при загрузке страницы
	handleScroll();
});