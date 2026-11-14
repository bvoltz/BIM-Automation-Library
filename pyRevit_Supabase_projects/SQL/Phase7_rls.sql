-- Step 2: Add owner_id column (each row belongs to a user)
alter table revit_models add column owner_id uuid references auth.users(id) default auth.uid();

-- Step 3A: Assign all existing rows to User A
-- Existing rows were created before owner_id existed, so they have no owner.
-- WHERE limits this to empty rows only (an UPDATE without WHERE changes every row).
update revit_models set owner_id = 'c90b9265-e187-4e63-8ec1-2b132c5aca77' where owner_id is null;

-- Step 3B: Make owner_id required
-- Every row must belong to a user. Without an owner, a row would be
-- hidden from everyone once RLS is on. This only succeeds if no row is still empty.
alter table revit_models alter column owner_id set not null;

-- Step 4: Turn on RLS on and remove the old policy
alter table revit_models enable row level security;

-- Step 4B: Delete the old policy that allow everyone to see every row
drop policy "allow_insert" on revit_models;


-- Step 5A: Add a new policy that allows users to view their models
create policy "Users can view their models" on revit_models
for select
to authenticated
using ( (select auth.uid()) = owner_id );

-- Step 5B: Add a new policy that allows users to add their models
create policy "Users can add their own models" on revit_models
for insert
to authenticated
with check ( (select auth.uid()) = owner_id );

-- Step 5C: Add a new policy that allows users to update their models
create policy "Users can update their models" on revit_models
for update
to authenticated
using ( (select auth.uid()) = owner_id )
with check ( (select auth.uid()) = owner_id );

-- Step 5D: Add a new policy that allows users to delete their models
create policy "Users can delete their models" on revit_models
for delete
to authenticated
using ( (select auth.uid()) = owner_id );