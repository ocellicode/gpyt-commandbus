[![Status][status-badge]][status-url]


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

# gpyt-commandbus

## About

## Getting started
Clone the repository, run `poetry install` in the repository root directory.

## Prerequisites
Python 3.11, pip, poetry.

## Installation
Installation of gpyt-commandbus is handled by poetry during development.

## Usage

Serve the application with `waitress-serve gpyt_commandbus.injection.injector:app`.

### Environment variables
| Variable      | Description          | Default                        |
|---------------|----------------------|--------------------------------|
| `GPYT_DB_DSN` | DSN for the database | `sqlite:///gpyt_commandbus.db` |
| `MIGRATE`     | Run migrations       | `0`                            |
| `LOG_LEVEL`   | Log level            | `INFO`                         |

[contributors-shield]: https://img.shields.io/github/contributors/ocellicode/gpyt-commandbus.svg?style=for-the-badge
[contributors-url]: https://github.com/ocellicode/gpyt-commandbus/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ocellicode/gpyt-commandbus.svg?style=for-the-badge
[forks-url]: https://github.com/ocellicode/gpyt-commandbus/network/members
[stars-shield]: https://img.shields.io/github/stars/ocellicode/gpyt-commandbus.svg?style=for-the-badge
[stars-url]: https://github.com/ocellicode/gpyt-commandbus/stargazers
[issues-shield]: https://img.shields.io/github/issues/ocellicode/gpyt-commandbus.svg?style=for-the-badge
[issues-url]: https://github.com/ocellicode/gpyt-commandbus/issues
[license-shield]: https://img.shields.io/github/license/ocellicode/gpyt-commandbus.svg?style=for-the-badge
[license-url]: https://github.com/ocellicode/gpyt-commandbus/blob/master/LICENSE
[status-badge]: https://github.com/ocellicode/gpyt-commandbus/actions/workflows/main.yml/badge.svg
[status-url]: https://github.com/ocellicode/gpyt-commandbus/actions/workflows/main.yml
