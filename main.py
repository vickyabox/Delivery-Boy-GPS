from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, ThreeLineIconListItem, IconLeftWidget
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.toast import toast
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
import webbrowser
from plyer import gps

class LocationApp(MDApp):
    dialog = None
    current_lat = None
    current_lon = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        self.store = JsonStore('saved_locations.json') # Data save karne ke liye

        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical')

        # Top Bar
        toolbar = MDTopAppBar(title="My Delivery Spots")
        toolbar.elevation = 10
        layout.add_widget(toolbar)

        # Scrollable List for saved locations
        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)

        # Floating Action Button (Add Button)
        fab = MDFloatingActionButton(
            icon="map-marker-plus",
            pos_hint={"center_x": 0.85, "center_y": 0.1},
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.show_add_dialog
        )
        
        screen.add_widget(layout)
        screen.add_widget(fab)
        
        self.load_saved_locations()
        return screen

    def on_start(self):
        # App start hote hi GPS connect karne ki koshish
        try:
            gps.configure(on_location=self.on_gps_location)
            gps.start(minTime=1000, minDistance=1) # Har 1 second mein update
        except NotImplementedError:
            toast("GPS feature not supported on this device type.")

    def on_stop(self):
        try:
            gps.stop()
        except:
            pass

    def on_gps_location(self, **kwargs):
        # Jab GPS se signal milega, ye chalega
        self.current_lat = kwargs.get('lat')
        self.current_lon = kwargs.get('lon')

    def load_saved_locations(self):
        # Save kiya hua data load karna
        self.list_view.clear_widgets()
        for key in self.store:
            data = self.store.get(key)
            self.add_item_to_list(key, data['notes'], data['coords'])

    def add_item_to_list(self, name, notes, coords):
        # List mein item dikhana
        item = ThreeLineIconListItem(
            text=name,
            secondary_text=notes if notes else "No notes",
            tertiary_text=coords,
            on_release=self.open_google_maps
        )
        icon = IconLeftWidget(icon="google-maps")
        item.add_widget(icon)
        self.list_view.add_widget(item)

    def show_add_dialog(self, instance):
        # Add karne wala popup box
        if not self.dialog:
            self.name_input = MDTextField(hint_text="Location Name (e.g., Sharma Ji)")
            self.notes_input = MDTextField(hint_text="Notes (e.g., 3rd Floor, Parcel leave at gate)")
            
            # Initial coordinate text
            coord_text = ""
            if self.current_lat and self.current_lon:
                 coord_text = f"{self.current_lat},{self.current_lon}"
            else:
                 coord_text = "Waiting for GPS... or type manually"
                 toast("GPS signal dhoond raha hoon. Bahar khade rahein.")

            self.coords_input = MDTextField(text=coord_text, hint_text="Coordinates (Lat,Lon)")

            content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="200dp")
            content.add_widget(self.name_input)
            content.add_widget(self.notes_input)
            content.add_widget(self.coords_input)

            self.dialog = MDDialog(
                title="Save Current Location",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                    MDRaisedButton(text="SAVE", on_release=self.save_location),
                ],
            )
        
        # Dialog khulte hi agar GPS data hai to update karo
        if self.current_lat and self.current_lon:
             self.coords_input.text = f"{self.current_lat},{self.current_lon}"
        
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss(force=True)
        self.dialog = None

    def save_location(self, instance):
        name = self.name_input.text
        notes = self.notes_input.text
        coords = self.coords_input.text

        if not name or not coords or "Waiting" in coords:
            toast("Naam aur Coordinates zaroori hain!")
            return

        # Data ko hamesha ke liye save karo
        self.store.put(name, notes=notes, coords=coords)
        self.add_item_to_list(name, notes, coords)
        self.close_dialog(instance)
        toast(f"{name} Saved!")

    def open_google_maps(self, list_item):
        # List par click karne par Google Maps kholna
        coords = list_item.tertiary_text
        if coords:
            # Google Maps navigation URL format
            url = f"google.navigation:q={coords}&mode=d"
            webbrowser.open(url)

LocationApp().run()
      
