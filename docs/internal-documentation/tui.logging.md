# tui.logging package

## Submodules

## tui.logging.tuiHandler module


### class tui.logging.tuiHandler.TuiHandler()
Bases: `logging.StreamHandler`


#### \__init__()
Initialize the handler.

If stream is not specified, sys.stderr is used.


#### configureModel(model)

#### emit(record)
Emit a record.

If a formatter is specified, it is used to format the record.
The record is then written to the stream with a trailing newline.  If
exception information is present, it is formatted using
traceback.print_exception and appended to the stream.  If the stream
has an ‘encoding’ attribute, it is used to determine how to do the
output to the stream.

## Module contents
