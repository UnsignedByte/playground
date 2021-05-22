/*
* @Author: UnsignedByte
* @Date:   2021-05-13 10:27:32
* @Last Modified by:   UnsignedByte
* @Last Modified time: 2021-05-13 11:22:33
*/

#include <vector>
#include <cstdio>

static int parse_cli(int argc, char** argv, std::vector<char*>& names, std::vector<char*>& values)
{
	int argi = -1;
	for(int i = 1; i < argc; i++)
	{
		char* word = argv[i];
		if (word[0] == '-') {
			word++; // remove "-" from the string
			argi++;
			// printf("Parsing argument name %s, index %d\n", word, argi);
			names.push_back(word);
			values.push_back(argv[++i]);
		} else {
			asprintf(&values[argi], "%s %s", values[argi], word);
			// printf("Updating argument value to %s\n", word);
		}
	}
	return argi+1;
}

int main(int argc, char** argv){
	std::vector<char*> names, values;
	int l = parse_cli(argc, argv, names, values);
	for (int i = 0; i < l; i++){
		printf("Argument %s (index %d) has value '%s'\n", names[i], i, values[i]);
	}
	return 0;
}