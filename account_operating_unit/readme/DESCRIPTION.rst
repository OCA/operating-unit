This module allows a company to manage the accounting based on Operating
Units (OU's).

* The financial reports (Trial Balance, P&L, Balance Sheet), allow to report
  the balances of one or more OU's.
* If a company wishes to report Balance Sheet and P&L accounts based on
  OU's, they should indicate at company level that the OU's are
  self-balanced, and the corresponding Inter-Operating Unit clearing account.
  The Chart of Accounts will always be balanced, for each Operating Unit.
* A company considering Operating Unit as applicable to report only profits
  and losses will not need to set the OU's as self-balanced.
* The self-balancing of Operating Unit is ensured at the time of posting a
  journal entry. In case that the journal involves posting of items in
  separate Operating Units, new journal items will be created, using the
  Inter-Operating Unit clearing account, to ensure that each OU is going to
  be self-balanced for that journal entry.
* Adds the Operating Unit to the invoice. A user can choose what OU to
  create the invoice for.
* Adds the Operating Unit to payments and payment methods. The operating
  unit of a payment will be that of the payment method chosen.
* Implements security rules at OU level to invoices, payments and journal
  items.
* Adds the Operating Unit to the cash basis journal entries.
