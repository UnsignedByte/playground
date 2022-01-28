MAIN := exe #output exe
CXXFLAGS := -MMD -MP -g -std=c++17
LDLIBS := -lglfw -lvulkan
# LDLIBS := -lsfml-graphics -lsfml-window -lsfml-system

.PHONY: all clean

all: $(MAIN)

$(MAIN): *.cpp *.hpp
	$(CXX) $(CXXFLAGS) *.cpp $(LDLIBS) -o $(MAIN)

clean:
	@$(RM) $(MAIN)