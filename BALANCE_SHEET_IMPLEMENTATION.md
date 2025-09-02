# Balance Sheet Implementation for ITICO

## Overview

This document describes the implementation of the Balance Sheet functionality for the ITICO contrapartes application. The Balance Sheet feature allows users to create, manage, and track financial statements for contrapartes, supporting both USD-only and multi-currency configurations.

## Features Implemented

### 1. Models

#### Moneda (Currency)
- **Purpose**: Manages different currencies available in the system
- **Fields**:
  - `codigo`: 3-character currency code (ISO 4217) - e.g., USD, EUR, COP
  - `nombre`: Full name of the currency
  - `simbolo`: Currency symbol (e.g., $, €, ¥)
  - `activo`: Boolean to indicate if currency is active
  - Audit fields: `creado_por`, `fecha_creacion`, `fecha_actualizacion`

#### TipoCambio (Exchange Rate)
- **Purpose**: Tracks historical exchange rates for currencies
- **Fields**:
  - `moneda`: Foreign key to Moneda
  - `tasa_usd`: Decimal field showing how many USD equals 1 unit of the currency
  - `fecha`: Date of the exchange rate
  - Audit fields: `creado_por`, `fecha_creacion`
- **Constraints**: Unique together constraint on `moneda` and `fecha`

#### BalanceSheet
- **Purpose**: Main model for Balance Sheets of contrapartes
- **Fields**:
  - `contraparte`: Foreign key to Contraparte
  - `año`: Year of the balance sheet
  - `solo_usd`: Boolean indicating if the balance sheet is USD-only
  - `moneda_local`: Optional foreign key to Moneda for local currency
  - `tipo_cambio`: Optional foreign key to TipoCambio for conversion rate
  - Audit fields: `creado_por`, `fecha_creacion`, `fecha_actualizacion`, `activo`
- **Constraints**: Unique together constraint on `contraparte` and `año`
- **Properties**:
  - `total_assets_usd`: Calculated total of all asset items
  - `total_liabilities_usd`: Calculated total of all liability items
  - `total_equity_usd`: Calculated total of all equity items

#### BalanceSheetItem
- **Purpose**: Individual line items within a Balance Sheet
- **Fields**:
  - `balance_sheet`: Foreign key to BalanceSheet
  - `descripcion`: Description of the line item
  - `nota`: Optional notes about the item
  - `categoria`: Choice field (Assets, Liabilities, Equity)
  - `monto_usd`: Amount in USD
  - `monto_local`: Optional amount in local currency
  - `orden`: Order for display purposes
  - Audit fields: `creado_por`, `fecha_creacion`, `fecha_actualizacion`, `activo`

### 2. Views

#### Balance Sheet Management
- `BalanceSheetListView`: Lists all balance sheets for a contraparte
- `BalanceSheetDetailView`: Shows detailed view of a balance sheet with categorized items
- `BalanceSheetCreateView`: Creates a new balance sheet
- `BalanceSheetUpdateView`: Edits balance sheet and its items using formsets
- `BalanceSheetDeleteView`: Soft deletes a balance sheet (sets `activo=False`)

#### Currency Management
- `MonedaListView`, `MonedaCreateView`, `MonedaUpdateView`, `MonedaDeleteView`: Full CRUD for currencies
- `TipoCambioListView`, `TipoCambioCreateView`, `TipoCambioUpdateView`, `TipoCambioDeleteView`: Full CRUD for exchange rates

#### AJAX Views
- `TipoCambioAjaxView`: Returns exchange rates for a specific currency (used for dynamic form updates)

### 3. Forms

#### Balance Sheet Forms
- `BalanceSheetForm`: Main form for balance sheet creation/editing
  - Includes dynamic behavior to show/hide currency fields based on `solo_usd` checkbox
  - Validates that if not USD-only, both local currency and exchange rate must be selected
- `BalanceSheetItemForm`: Form for individual balance sheet items
  - Disables local currency field when balance sheet is USD-only
- `BalanceSheetItemFormSet`: Django formset for managing multiple items

#### Currency Forms
- `MonedaForm`: Form for creating/editing currencies
- `TipoCambioForm`: Form for creating/editing exchange rates

### 4. Templates

#### Balance Sheet Templates
- `balance_sheet_lista.html`: Lists balance sheets with summary information
- `balance_sheet_crear.html`: Form for creating new balance sheets
- `balance_sheet_editar.html`: Complex form with JavaScript for editing balance sheets and their items
- `balance_sheet_detalle.html`: Detailed view showing categorized items and balance verification
- `balance_sheet_eliminar.html`: Confirmation page for deletion

#### Currency Templates
- `moneda_lista.html`: Lists all currencies with management options

### 5. URLs

New URL patterns added to `contrapartes/urls.py`:

```python
# Balance Sheets
path('<int:contraparte_pk>/balance-sheets/', views.BalanceSheetListView.as_view(), name='balance_sheet_lista'),
path('<int:contraparte_pk>/balance-sheets/crear/', views.BalanceSheetCreateView.as_view(), name='balance_sheet_crear'),
path('balance-sheets/<int:pk>/', views.BalanceSheetDetailView.as_view(), name='balance_sheet_detalle'),
path('balance-sheets/<int:pk>/editar/', views.BalanceSheetUpdateView.as_view(), name='balance_sheet_editar'),
path('balance-sheets/<int:pk>/eliminar/', views.BalanceSheetDeleteView.as_view(), name='balance_sheet_eliminar'),

# AJAX endpoints
path('ajax/tipos-cambio/', views.TipoCambioAjaxView.as_view(), name='tipos_cambio_ajax'),

# Currency management
path('monedas/', views.MonedaListView.as_view(), name='moneda_lista'),
path('monedas/crear/', views.MonedaCreateView.as_view(), name='moneda_crear'),
path('monedas/<int:pk>/editar/', views.MonedaUpdateView.as_view(), name='moneda_editar'),
path('monedas/<int:pk>/eliminar/', views.MonedaDeleteView.as_view(), name='moneda_eliminar'),

# Exchange rate management
path('tipos-cambio/', views.TipoCambioListView.as_view(), name='tipo_cambio_lista'),
path('tipos-cambio/crear/', views.TipoCambioCreateView.as_view(), name='tipo_cambio_crear'),
path('tipos-cambio/<int:pk>/editar/', views.TipoCambioUpdateView.as_view(), name='tipo_cambio_editar'),
path('tipos-cambio/<int:pk>/eliminar/', views.TipoCambioDeleteView.as_view(), name='tipo_cambio_eliminar'),
```

### 6. Admin Interface

Full Django admin configuration for all new models:
- `MonedaAdmin`: Manages currencies with search and filtering
- `TipoCambioAdmin`: Manages exchange rates with date hierarchy
- `BalanceSheetAdmin`: Manages balance sheets with inline items
- `BalanceSheetItemAdmin`: Manages individual balance sheet items

### 7. Management Command

`setup_balance_sheet_data.py`: Creates initial currencies and sample exchange rates:
- 9 common currencies (USD, COP, EUR, GBP, JPY, BRL, MXN, PEN, CLP)
- Historical exchange rates for each currency (3 dates in 2024)

## Usage Workflow

### 1. Setting Up Currencies and Exchange Rates

1. **Initial Setup**: Run the management command to populate initial data:
   ```bash
   python manage.py setup_balance_sheet_data
   ```

2. **Manage Currencies**: Access via admin or the currency management views to add/edit currencies

3. **Update Exchange Rates**: Regularly update exchange rates for accurate conversions

### 2. Creating a Balance Sheet

1. **Access from Contraparte Detail**: Click "Balance Sheets" in the sidebar
2. **Create New Balance Sheet**: 
   - Specify the year
   - Choose between USD-only or multi-currency
   - If multi-currency, select local currency and exchange rate
3. **Add Items**: After creation, edit the balance sheet to add line items in three categories:
   - Assets
   - Liabilities
   - Equity

### 3. Managing Balance Sheet Items

The editing interface provides:
- Dynamic form addition for new items
- Categorized display (Assets, Liabilities, Equity)
- Real-time total calculations
- Balance verification (Assets = Liabilities + Equity)

### 4. Viewing and Analysis

The detail view shows:
- Summary cards with totals
- Items grouped by category
- Balance verification
- Currency configuration details
- Metadata about creation and updates

## JavaScript Features

### Dynamic Form Behavior

1. **Currency Selection**: 
   - Checkbox toggles between USD-only and multi-currency
   - Local currency field populates exchange rate options via AJAX

2. **Item Management**:
   - Add new items dynamically
   - Real-time calculation of category totals
   - Items are grouped visually by category

3. **Form Validation**:
   - Client-side validation for required fields
   - Balance verification feedback

## Database Migrations

The implementation required one migration:
- `0028_balancesheet_balancesheetitem_moneda_and_more.py`: Creates all new models and relationships

## Security Considerations

1. **Authentication**: All views require login (`LoginRequiredMixin`)
2. **Authorization**: Users can only access balance sheets for contrapartes they have permission to view
3. **Audit Trail**: All models include audit fields to track who created/modified records
4. **Soft Deletion**: Balance sheets are soft-deleted (marked inactive) to preserve historical data

## Performance Optimizations

1. **Database Queries**:
   - Calculated properties use aggregation queries
   - Foreign key relationships are properly indexed
   - Select/prefetch related used where appropriate

2. **Caching**:
   - Exchange rate lookups are efficient with proper indexing
   - Category totals are calculated on-demand but could be cached if needed

## Future Enhancements

Potential improvements could include:

1. **Import/Export**: CSV or Excel import/export for balance sheet data
2. **Automatic Exchange Rates**: Integration with external APIs for real-time rates
3. **Historical Analysis**: Trend analysis across multiple years
4. **Validation Rules**: Custom validation for balance sheet consistency
5. **Templates**: Pre-defined balance sheet templates for different industries
6. **Approval Workflow**: Multi-step approval process for balance sheets
7. **Notifications**: Email notifications for balance sheet updates
8. **Reporting**: PDF generation for formatted balance sheet reports

## Testing

To test the implementation:

1. **Manual Testing**:
   - Create a contraparte
   - Access the balance sheet section
   - Create both USD-only and multi-currency balance sheets
   - Add various types of items
   - Verify calculations and balance verification

2. **Data Integrity**:
   - Verify unique constraints work correctly
   - Test soft deletion behavior
   - Confirm audit trail functionality

3. **UI/UX**:
   - Test responsive design on different screen sizes
   - Verify JavaScript functionality works across browsers
   - Test form validation behavior

## Dependencies

The implementation uses existing Django/Python dependencies:
- Django forms and formsets
- Django admin
- Decimal for precise financial calculations
- Standard Django authentication and permissions

No additional external dependencies were introduced.
