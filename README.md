# tick

Python scripts to assist with filling out TickSpot using the request module. Information on the project, task and entries can be queried
through simple commands. Entries can also be created with this information.

## Installation

Install directly from GitHub as follows:

```bash
pip install git+https://github.com/andrewbeattie/tick.git
```

You will need to add the following to your environment variables.

```bash
TICKSPOT_USERNAME
TICKERSPOT_PASSWORD
```

You will need to save this file and create the environment variable "TICKSPOT_CONFIG" pointing towards the config file.

## Usage

![ ](https://i.imgur.com/aapxUnH.png)

1. Use list project to get the project id
2. Use the project id to use list task to get the appropriate task id
3. Create an entry with a project id and task id.

## Examples

`ticker list project`: lists all projects in TickSpot
`ticker list task 11934`: lists all tasks for project with ID 11934
`ticker create -p 1955215 -t 14519343 -ho 8 -d 2021-10-11`: creates a time entry for 8 hours on 2021-10-11 for task with ID 14519343 in project with ID 1955215
`ticker start -p <project> -t <task> -m <summary>`: starts a new time entry for the specified project and task with the given summary
`ticker list time -p`: lists all time entries for the current day for all projects

## License

[MIT](https://choosealicense.com/licenses/mit)
