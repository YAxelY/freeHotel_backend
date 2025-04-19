basic make file structure if you just import make , it would execute the first command namely "all" 

    # Makefile

    .PHONY: all updateRequirements test

    # default goal when you just run `make`
    all: updateRequirements

    # regenerate requirements.txt
    updateRequirements:
        @echo "🔧 Generating requirements.txt…"
        pip freeze > requirements.txt
        @echo "✅ requirements.txt updated"

    # example other target
    test:
        pytest
