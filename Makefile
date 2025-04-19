# Makefile

.PHONY: updateRequirements

updateRequirements:
	@echo "🔧 Generating requirements.txt…"
	pip freeze > requirements.txt
	@echo "✅ requirements.txt updated"
