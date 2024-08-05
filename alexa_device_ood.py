"""
QUESTION

 Alexa devices come in a variety of options

 * Some have screens & speakers, some only screens or speakers and some with none of them
 * Some come with batteries, some only wall plugin, some with batteries and wall plugins


 Design a set of classes that will report the current battery/power status to the user.
 Depending on the hardware, the response may need to be spoken,
 or displayed on a screen, or both.
 Also, depending on whether there is a battery or not, the status message will differ.

 For example, if the device is a Tablet which has a battery, a speaker, and a display,
 and currently it happens to be plugged in and recharging (let's say at 75%),
 then your code should return the following:
 * Say "Current battery level is 75% and charging" through the speaker.
 * Display "Current battery level is 75% and charging" on the screen.

 Whereas if the device is an Echo Dot, which has a speaker but no battery and no screen, then your code should only return:
 * Say "Currently plugged into wall power" through the speaker.
 and should NOT attempt to display anything (since there is no screen).

 For simplicity, ignore the details of speech generation and image/visual card generation -
 we can safely assume those are provided. Focus more on modeling the Alexa devices and their properties,
 and returning the correct responses.

 What if we need to support more UI modalities and more system features:

 * More power supplies: charging pad, removable batteries, Alexa-enabled Smart Home wall plug, etc.
 * Additional speakers: Bluetooth or Aux or Wi-Fi connected speakers
 * Additional outputs: LED light ring (changes colour), text/SMS/notifications, etc.

 How do you prevent the "combinatorial explosion" of all the possible status messages x delivery mechanisms?
"""
from abc import ABC, abstractmethod
from typing import Optional, List


class Message:
    def __init__(self, message):
        self.message = message


# abstract classes for audio video options
# class AudioOption(ABC):
#     @abstractmethod
#     def speak(self, message:Message):
#         pass
#
#
# class VisualOption(ABC):
#     @abstractmethod
#     def display(self, message: Message):
#         pass
#

class OutputOptions(ABC):
    @abstractmethod
    def send_message(self, message:Message):
        pass


class Screen(VisualOption, OutputOptions):
    def send_message(self, message: Message):
        self.display(message)

    def display(self, message: Message):
        print(f"Displaying: {message.message}")


class Speaker(AudioOption, OutputOptions):
    def send_message(self, message: Message):
        self.speak(message)

    def speak(self, message: Message):
        print(f"Speaking: {message.message}")


class PowerSource(ABC):
    @abstractmethod
    def generate_message(self):
        pass


class Battery(PowerSource):

    # @staticmethod
    # def get_power_level():
    #     power_level = PowerOutlet.get_power_level()
    #     return power_level

    def generate_message(self):
        # return Message(f"Current Battery level is {PowerOutlet.power_level} and charging")
        return Message(f"Current Battery level is 70% and charging")


class WallPlugin(PowerSource):

    def generate_message(self):
        return Message(f"Currently plugged into wall plugin and charging")


class AlexaDevice(ABC):
    @abstractmethod
    def __init__(self, av:List[OutputOptions], power:List[PowerSource] ):
        self.av: List[OutputOptions] = av
        self.power: List[PowerSource] = power
        self.connected_power_source: Optional[PowerSource] = None

    def output(self, connected_power_source:PowerSource):
        for option in self.av:
            option.send_message(connected_power_source.generate_message() if self.connected_power_source \
                                else Message("Not connected to power source"))

    def set_connected_power_source(self, connected_source):
        self.connected_power_source = connected_source


class EchoDot(AlexaDevice):
    def __init__(self, av: List[OutputOptions], power: List[PowerSource]):
        super().__init__(av, power)


class Tablet(AlexaDevice):
    def __init__(self, av: List[OutputOptions], power: List[PowerSource]):
        super().__init__(av, power)


if __name__ == "__main__":

    tablet_output_options: List[OutputOptions] = [Screen(), Speaker()]
    tablet_power_source: List[PowerSource] = [Battery()]

    my_tablet: Tablet = Tablet(tablet_output_options, tablet_power_source)
    my_tablet.set_connected_power_source(tablet_power_source[0])

    echodot_output_options: List[OutputOptions] = [Speaker()]
    echodot_power_source: List[PowerSource] = [WallPlugin()]

    my_echodot: EchoDot = EchoDot(echodot_output_options, echodot_power_source)
    my_echodot.set_connected_power_source(echodot_power_source[0])

    print("My echo dot status:")
    my_echodot.output(my_echodot.connected_power_source)
    print("My tablet status:")
    my_tablet.output(my_tablet.connected_power_source)








