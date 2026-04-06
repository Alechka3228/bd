Select sum(P.weight) FROM
  "Rooms" R Join "Racks" Ra On Ra.room_id = room.id
  Join "Storages" S On S.shelf_id = Ra.shelf_id
  Join "Products" P On S.storage_id = P.storage_id;
