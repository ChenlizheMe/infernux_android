# Keep release-engineering symbols outside the installable package. The original
# build outputs remain untouched, and runtime dynamic symbols remain available.
file(MAKE_DIRECTORY "${PLAYER_DIR}/jniLibs" "${SYMBOLS_DIR}")
string(REPLACE "|" ";" _libraries "${PLAYER_FILES}")
foreach(_source IN LISTS _libraries)
    get_filename_component(_name "${_source}" NAME)
    set(_runtime "${PLAYER_DIR}/jniLibs/${_name}")
    set(_symbols "${SYMBOLS_DIR}/${_name}.debug")
    execute_process(COMMAND "${OBJCOPY}" --only-keep-debug "${_source}" "${_symbols}"
        COMMAND_ERROR_IS_FATAL ANY)
    execute_process(COMMAND "${STRIP}" --strip-debug -o "${_runtime}" "${_source}"
        COMMAND_ERROR_IS_FATAL ANY)
    execute_process(COMMAND "${OBJCOPY}" "--add-gnu-debuglink=${_symbols}" "${_runtime}"
        COMMAND_ERROR_IS_FATAL ANY)
endforeach()
