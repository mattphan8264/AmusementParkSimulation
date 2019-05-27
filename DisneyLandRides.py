from DisneyLandSimulation import AmusementRide
import numpy as N

Space_Mountain = AmusementRide(5, 163)
Indiana_Jones_Adventure = AmusementRide(10, 352)
Matterhorn_Bobsleds = AmusementRide(4, 115)
Pirates_of_the_Caribbean = AmusementRide(15, 773)
Big_Thunder_Mountain_Railroad = AmusementRide(3.5, 128)
Autopia = AmusementRide(4.5, 213)
Star_Tours_The_Adventures_Continue = AmusementRide(7, 169)
Haunted_Mansion = AmusementRide(9, 369)
Splash_Mountain = AmusementRide(11, 261)
Jungle_Cruise = AmusementRide(7.5, 246)
Its_a_Small_World = AmusementRide(14, 583)
Storybook_Land_Canal_Boats = AmusementRide(9.5, 237)
Finding_Nemo_Submarine_Voyage = AmusementRide(13, 184)
Peter_Pans_Flight = AmusementRide(3, 28)
The_Many_Adventures_of_Winnie_The_Pooh = AmusementRide(4, 143)
Alice_in_Wonderland = AmusementRide(4, 40)
Mad_Tea_Party = AmusementRide(1.5, 27)
Astro_Orbiter = AmusementRide(1.5, 16)
Dumbo_the_Flying_Elephant = AmusementRide(1.67, 16)
Buzz_Lightyear_Astro_Blasters = AmusementRide(4.5, 45)
King_Arthur_Carrousel = AmusementRide(3, 60)
Mark_Twain_Riverboat = AmusementRide(18, 360)
Gadgets_Go_Coaster = AmusementRide(1, 10)
Snow_Whites_Scary_Adventures = AmusementRide(2, 20)
Mr_Toads_Wild_Ride = AmusementRide(2, 16)
Pinocchios_Daring_Journey = AmusementRide(3, 30)
Sailing_Ship_Columbia = AmusementRide(14, 210)
Casey_Jr_Circus_Train = AmusementRide(4, 24)
Roger_Rabbits_Car_Toon_Spin = AmusementRide(4, 19)
Davey_Crocketts_Explorer_Canoes = AmusementRide(10, 100)

def getAllRides():
    return N.asarray(
        [Space_Mountain, Indiana_Jones_Adventure, Matterhorn_Bobsleds,
        Pirates_of_the_Caribbean, Big_Thunder_Mountain_Railroad,
        Autopia, Star_Tours_The_Adventures_Continue, Haunted_Mansion,
        Splash_Mountain, Jungle_Cruise, Its_a_Small_World,
        Storybook_Land_Canal_Boats, Finding_Nemo_Submarine_Voyage,
        Peter_Pans_Flight, The_Many_Adventures_of_Winnie_The_Pooh,
        Alice_in_Wonderland, Mad_Tea_Party, Astro_Orbiter,
        Dumbo_the_Flying_Elephant, Buzz_Lightyear_Astro_Blasters,
        King_Arthur_Carrousel, Mark_Twain_Riverboat, Gadgets_Go_Coaster,
        Snow_Whites_Scary_Adventures, Mr_Toads_Wild_Ride,
        Pinocchios_Daring_Journey, Sailing_Ship_Columbia, Casey_Jr_Circus_Train,
        Roger_Rabbits_Car_Toon_Spin, Davey_Crocketts_Explorer_Canoes])

if __name__ == "__main__":
    print(getAllRides())