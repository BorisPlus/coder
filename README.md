# Задача кодирования данных в ограниченном объеме

## Ситуация

* Протоколом взаимодействия клиента и сервера для передачи параметров запроса отведен __ограниченный__ по размеру блок данных.
* Cодержание и обработка блока параметров запроса остается на усмотрение разработчика, реализующего данные клиент и сервер.

## Задача

* Подобрать механизм кодирования параметров запроса в условии __ограниченного__ размера отведенного для них блока.
* (Опционально) оценить удобство использования механизма кодирования сторонними разработчиками.

## Идея

Распространенным форматом передачи структур является `JSON`, однако в данном случае он избыточен, так как названия свойств, а также разделители "свойство-свойство" и "ключ-значение" отнимут __драгоценные__ байты данных.

Решено сравнить объемы данных:

* сугубо строкового `*SV`-формата (`CSV`, `TSV` и пр. `SV`) кодирования без поддержки типизации;
* бинарных форматов кодирования, обеспечивающих их типизацию:
  * Pickle;
  * ProtoBuf;
  * FlatBuffers.

## Проведение исследования

* [Данные для тестирования](facets.py).
* *SV - [Класс параметров](sv/params.py) и [тестирование варианта SV-кодирования](sv/test.py).
* Pkl - [Тестирование варианта Pickle-кодирования всего объекта](pickle/test.py).
* Pkl* - [Тестирование варианта Pickle-кодирования кортежа значений полей, а не всего объекта](pickle_tuple/test.py).
* PB - [ProtoBuf-объект параметров](protobuf/params.proto) и [тестирование варианта ProtoBuf-кодирования](protobuf/test.py).
  
_Замечание_:

```shell
# Создание Python-класса из ProtoBuf-объекта
protoc -I=./protobuf --python_out=./protobuf ./protobuf/params.proto
```

* FB - [FlatBuffers-объект параметров](flatbuffers/params.fbs) и [тестирование варианта FlatBuffers-кодирования](flatbuffers/test.py).

_Замечание_:

```shell
# Создание Python-класса из FlatBuffers-объекта
 ../../flatbuffers/flatc -o flatbuffers --python flatbuffers/params.fbs
```

_Замечание:_ [Установка FlatBuffers](https://stackoverflow.com/a/55394568/24858592)

_Замечание:_ [Оригинальный FlatBuffers-пример](https://flatbuffers.dev/flatbuffers_guide_tutorial.html)

## Вывод о размерах

| Params and buffer size                                                            | *SV | Pkl | Pkl* | PB  | FB  |
| --------------------------------------------------------------------------------- | --- | --- | ---- | --- | --- |
| {'number': 1, 'string': '', 'bytes': b''}                                         | 3   | 92  | 19   | 6   | 44  |
| {'number': 1, 'string': 't', 'bytes': b'b'}                                       | 5   | 94  | 21   | 8   | 48  |
| {'number': 1, 'string': 'text_0123456', 'bytes': b'bytes_0'}                      | 22  | 111 | 38   | 25  | 64  |
| {'number': 10, 'string': 'text_0123456', 'bytes': b'bytes_0'}                     | 23  | 111 | 38   | 25  | 64  |
| {'number': 10, 'string': 'text_0123456', 'bytes': b'bytes_01'}                    | 24  | 112 | 39   | 26  | 64  |
| {'number': 10, 'string': 'text_01234567', 'bytes': b'bytes_01'}                   | 25  | 113 | 40   | 27  | 64  |
| {'number': 17, 'string': 'text_0123456', 'bytes': b'bytes_01'}                    | 24  | 112 | 39   | 26  | 64  |
| {'number': 1000000000, 'string': 'text_0123456789', 'bytes': b'bytes_0123456789'} | 43  | 126 | 53   | 41  | 72  |

В целом, использовать `ProtoBuf` выгоднее как по причине небольшого объема формируемого буфера данных, так и, что на мой взгляд важнее, в связи со строгой типизации полей данных (если клиент ожидает `int`, то нет необходимости об этом заботиться вручную, конвертируя `string` в `int`).

_Замечание_: на больших объемах данных сжатие поля очевидно было бы эффективно, однако, в условии его ограниченной длины архивирование имеет негативный эффект (тестировалось для `gzip`, `zlib`, `bz2`, `lzma`).

## Вывод об удобстве использования

Закрепив один из механизмов кодирования в качестве догмы в неком фреймворке, на базе которого планируется реализовывать клиенты и серверы, очень важным фактором является порог вхождения разработчика-пользователя. На сколько удобен/прозрачен тот или иной подход для стороннего разработчика?

Рассуждение:

* Достаточно сложно инкапсулировать в фреймворке логику создания Python-классов при использовании `FlatBuffers` и `ProtoBuf`, без необходимости погружения разработчика в синтаксис и использования им `*.fbs` и `*.proto`.
* В случае `SV` кодирования разработчик сильно фокусируется на типах сериализуемых и десериализуемых данных.
* Достаточно прозрачным выглядит `Pickle` для `Python`-разработчика и более-менее экономно `Pickle-tuple`. Он не требует дополнительных библиотек. Инкапсулировать логику кодирования произвольных параметров достаточно просто.

Итоговое ранжирование по уровню "удобства" использования тесно связано с возможностью формализации механизма в фреймворке (приведено по степени увеличение порога вхождения):

* Pickle;
* Pickle-tuple;
* Separated Value;
* FlatBuffers.
* ProtoBuf.

### Иные варианты сериализации

* [Список протоколов](https://en.wikipedia.org/wiki/Comparison_of_data-serialization_formats)
