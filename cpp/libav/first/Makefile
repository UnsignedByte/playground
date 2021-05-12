MAIN := exe #output exe
IN := first.cpp
LDLIBS := -lavcodec -lavformat -lavutil
# LDLIBS := -lsfml-graphics -lsfml-window -lsfml-system

.PHONY: all clean

all: $(MAIN)

$(MAIN): $(IN)
	$(CXX) $(IN) $(LDLIBS) -o $(MAIN)

clean:
	@$(RM) $(MAIN)