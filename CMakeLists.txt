project(cmak_py_gen)
cmake_minimum_required(VERSION 3.22)

find_package (Python COMPONENTS Interpreter Development)
find_program (PIPX pipx)

if(not ${PIPX})
  message("Not Found PIPX")
endif()


execute_process(COMMAND ${Python_EXECUTABLE} -m pip install --target ${CMAKE_BINARY_DIR}/pipx pipx)

function(build_python_cli target package)
  message("pipx install -e ${package}")
  add_custom_target(${target}
	COMMAND ${CMAKE_COMMAND} -E 
		env PIPX_HOME=${CMAKE_BINARY_DIR}/pipx_venv 
		env PIPX_BIN_DIR=${CMAKE_BINARY_DIR}/bin 
		${CMAKE_BINARY_DIR}/pipx/bin/pipx install -e ${package})
endfunction()

build_python_cli(build_gen_py ${CMAKE_SOURCE_DIR}/pygen)

add_custom_command(OUTPUT gen.h
	COMMAND ${CMAKE_BINARY_DIR}/bin/genfile
	WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
	DEPENDS build_gen_py)

add_custom_target(gen_file DEPENDS gen.h)

add_executable(run main.c)
add_dependencies(run gen_file)
