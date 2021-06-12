# @Author: almundmilk
# @Date:   2021-06-11 20:15:00
# @Last Modified by:   almundmilk
# @Last Modified time: 2021-06-11 20:21:04

alias glslc="/usr/bin/glslc"

declare -a shaders=("simple_shader.vert" "simple_shader.frag")

for shader in "${shaders[@]}"; do
	echo "compiling $shader"
	glslc "shaders/$shader" -o "shaders/$shader.spv"
done