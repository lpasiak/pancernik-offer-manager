from connections.shoper_connect import ShoperAPIClient
from connections.shoper.redirects import ShoperRedirects
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
import pandas as pd
from utils.logger import get_outlet_logger
from tqdm import tqdm


class OutletRedirectRemover:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_redirects = None
        self.gsheets_worksheets = None
        self.outlet_logger = get_outlet_logger().get_logger()
        
    def connect(self):
        """Initialize all necessary connections"""
        try:
            # Initialize Shoper connections
            self.shoper_client = ShoperAPIClient(
                config.SHOPER_SITE_URL,
                config.SHOPER_LOGIN,
                config.SHOPER_PASSWORD
            )
            self.shoper_client.connect()
            self.shoper_redirects = ShoperRedirects(self.shoper_client)
            
            # Initialize Google Sheets connections
            self.gsheets_client = GSheetsClient(
                config.GOOGLE_CREDENTIALS_FILE,
                config.OUTLET_SHEET_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing connections: {e}")
            self.outlet_logger.warning(f"❌ Error initializing connections: {e}")
            return False
        
    def select_redirects_to_remove(self):
        """Get all redirects that have been created more than 21 days ago.
        Returns:
            A pandas DataFrame containing the redirects to be removed or None if no redirects are found
        """
        today = pd.Timestamp.today()

        df = self.gsheets_worksheets.get_data(sheet_name=config.OUTLET_SHEET_ARCHIVED_NAME, include_row_numbers=True)

        df['Data usunięcia'] = pd.to_datetime(
            df['Data usunięcia'], 
            format='%d-%m-%Y',
            errors='coerce'
        )

        days_difference = (today - df['Data usunięcia']).dt.days

        mask = (
            (days_difference >= config.OUTLET_REDIRECT_DAYS_TO_BE_REMOVED) &
            (df['ID Przekierowania'].notna()) &
            (df['ID Przekierowania'] != '') &
            (df['Data usunięcia'].notna())
        )

        df = df[mask]

        print(f'ℹ️  Selected redirects ready to be removed: {len(df)}')
        self.outlet_logger.info(f'ℹ️ Selected redirects ready to be removed: {len(df)}')

        if len(df) > 0:
            return df
        return None
    
    def remove_redirects(self):
        """Remove redirects that are 3-week or later
        
        Returns:
            number of created redirects
        """

        df_redirects_to_remove = self.select_redirects_to_remove()

        if df_redirects_to_remove is None or df_redirects_to_remove.empty:
            return
        
        redirects_to_be_removed_counter = len(df_redirects_to_remove)
        redirects_removed_counter = 0
        gsheets_updates = []

        for index, product in tqdm(df_redirects_to_remove.iterrows(), 
                                   total=redirects_to_be_removed_counter,
                                   desc="Removing redirects",
                                   unit=" redirect"):
            
            google_sheets_row = product['Row Number']
            redirect_code = product['ID Przekierowania']

            # Remove a redirect
            response = self.shoper_redirects.remove_redirect(redirect_code)

            if response == True:
                self.outlet_logger.info(f'✅ Removed redirect with ID: {redirect_code}')
                redirects_removed_counter += 1

                if google_sheets_row is not None:
                    gsheets_updates.append([google_sheets_row, ''])

        self.batch_update_removed_redirects_gsheets(gsheets_updates)

        return redirects_removed_counter
    
    def batch_update_removed_redirects_gsheets(self, gsheets_updates):
        """Update removed redirects on Google Sheet
        Args:
            gsheets_updates (list): A gsheet row number and a value to override the redirect ID
        """
        try:
            self.gsheets_worksheets.batch_update_from_a_list(
                worksheet_name=config.OUTLET_SHEET_ARCHIVED_NAME,
                updates=gsheets_updates,
                start_column='N',
                num_columns=1
            )
        except Exception as e:
            print(f'❌ Failed to update Google Sheets: {str(e)}')
            self.outlet_logger.critical(f'❌ Failed to update Google Sheets: {str(e)}')
